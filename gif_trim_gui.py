import argparse
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import threading
import time

#flag to indicate if the process should be canceled
cancel_flag = threading.Event()  

def find_duplicate_frame(gif_path):
    #open the gif file
    gif = Image.open(gif_path)

    #get the first frame
    gif.seek(0)  #move to the first frame
    first_frame = gif.convert('RGB')  #convert the first frame to rgb

    #total number of frames in the gif
    total_frames = gif.n_frames

    #compare each subsequent frame with the first frame
    for i in range(1, total_frames):  #start from the second frame
        gif.seek(i)  #move to the i-th frame
        current_frame = gif.convert('RGB')  #convert the current frame to rgb

        log_box.insert(tk.END, f"Checking Frame {i+1} / {total_frames}...\n")
        log_box.yview(tk.END)  #scroll to the bottom

        #periodically check for cancellation
        if cancel_flag.is_set():
            log_box.insert(tk.END, "Process canceled by user.\n")
            log_box.yview(tk.END)
            return -1  #stop processing if the cancel flag is set

        #compare the current frame with the first frame
        if list(current_frame.getdata()) == list(first_frame.getdata()):
            log_box.insert(tk.END, f"Frame {i+1} is identical to the first frame.\n")
            log_box.yview(tk.END)
            return i + 1  #return the frame number of the duplicate

    log_box.insert(tk.END, "No identical frame found.\n")
    log_box.yview(tk.END)
    
    #show a popup and terminate the program if no loop is found
    messagebox.showinfo("No Loop Found", "No loop could be found in the GIF.")
    log_box.insert(tk.END, "No loop could be found in the GIF.\n")
    log_box.yview(tk.END)

    sys.exit()  #terminate the process immediately

def create_new_gif(input_gif_path, output_gif_path, end_frame):
    #open the original gif
    gif = Image.open(input_gif_path)

    #total number of frames in the gif
    total_frames = gif.n_frames

    #ensure that the 'end_frame' doesn't exceed the total number of frames
    if end_frame > total_frames:
        log_box.insert(tk.END, f"End frame {end_frame} exceeds the total number of frames ({total_frames}).\n")
        log_box.yview(tk.END)
        return

    #list to store the frames for the new gif
    frames = []

    #extract frames from the 1st to (end_frame-1)th frame
    for i in range(end_frame - 1):  #go up to the end_frame-1
        gif.seek(i)  #move to the i-th frame
        frames.append(gif.copy())  #append the current frame to the list
        log_box.insert(tk.END, f"Trimming Frame {i + 1}...\n")
        log_box.yview(tk.END)  #scroll to the bottom

        #periodically check for cancellation
        if cancel_flag.is_set():
            log_box.insert(tk.END, "Process canceled by user.\n")
            log_box.yview(tk.END)
            return

    #save the new gif
    log_box.insert(tk.END, f"Creating GIF (this can take a while)\n")
    log_box.yview(tk.END)

    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], duration=gif.info['duration'], loop=0)

    #show a popup when the new GIF is created successfully
    messagebox.showinfo("Process Complete", f"Trimmed GIF created at {output_gif_path}")

    #print out the results in the log_box
    log_box.insert(tk.END, f"Trimmed GIF created at {output_gif_path}\n")
    log_box.yview(tk.END)

    #re-enable buttons and grey out the cancel button after process finishes
    trim_button.config(state=tk.NORMAL, bg='green')
    open_button.config(state=tk.NORMAL, bg='green')
    cancel_button.config(state=tk.DISABLED, bg='yellow')

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        gif_path.set(file_path)
        log_box.insert(tk.END, f"Selected file: {file_path}\n")
        log_box.yview(tk.END)

        #make buttons green after GIF selected
        trim_button.config(bg='green')
        open_button.config(bg='green')

def process_gif():
    gif_path_str = gif_path.get()
    if not gif_path_str:
        log_box.insert(tk.END, "Error: No GIF file selected.\n")
        log_box.yview(tk.END)
        return

    #disable buttons and show the cancel button while processing
    trim_button.config(state=tk.DISABLED, bg='yellow')
    open_button.config(state=tk.DISABLED, bg='gray')
    cancel_button.config(state=tk.NORMAL, bg='red')

    cancel_flag.clear()  #clear any previous cancel flag

    #find the duplicate frame
    duplicate_frame = find_duplicate_frame(gif_path_str)

    if duplicate_frame == -1:
        # "No loop could be found" case
        log_box.insert(tk.END, "No identical frame found. The entire GIF will be used.\n")
        log_box.yview(tk.END)
        messagebox.showinfo("No Loop Found", "No loop could be found in the GIF.")
        sys.exit()  #terminate immediately

    log_box.insert(tk.END, f"Duplicate found at frame {duplicate_frame}.\n")
    log_box.yview(tk.END)
    end_frame = duplicate_frame

    #define the output gif path (same location as input gif)
    output_gif_path = gif_path_str.rsplit('.', 1)[0] + "_trimmed.gif"

    #create the new gif
    create_new_gif(gif_path_str, output_gif_path, end_frame)

def cancel_process():
    cancel_flag.set()  #set the cancel flag to stop the process
    log_box.insert(tk.END, "Process canceled by user.\n")
    log_box.yview(tk.END)
    cancel_button.config(state=tk.DISABLED, bg='yellow') 
    trim_button.config(state=tk.NORMAL, bg='green')
    open_button.config(state=tk.NORMAL, bg='green')

def start_process_in_thread():
    #run the process in a background thread
    threading.Thread(target=process_gif, daemon=True).start()

def drop_event(event):
    gif_path.set(event.data)
    log_box.insert(tk.END, f"File dropped: {event.data}\n")
    log_box.yview(tk.END)

    #change trim button to green after a GIF is selected
    trim_button.config(bg='green')

    #change "Open GIF Here" button to green after a GIF is selected
    open_button.config(bg='green')


#tkinter gui setup with drag and drop
root = TkinterDnD.Tk()
root.title("GIF Looping Trim Tool")

#set window size
root.geometry("420x395")
root.resizable(False, False)

#define logo_path before checking its existence
logo_path = "gif_trim_logo.png"

#check if the logo file exists and use it as the app icon if it's a PNG image
if os.path.isfile(logo_path):
    logo = Image.open(logo_path)
    logo = logo.resize((150, 150))  #resize to fit the space
    logo = ImageTk.PhotoImage(logo)
    root.iconphoto(False, logo)  #set the PNG image as the app icon

#create a frame for the logo and buttons using grid
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

#add the logo on the left
if os.path.isfile(logo_path):
    logo_label = tk.Label(top_frame, image=logo)
    logo_label.grid(row=0, column=0, padx=10, sticky="n")

#create a frame for the buttons and filepath, aligned vertically
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

#create the "open gif here" button (starts yellow)
open_button = tk.Button(button_frame, text="Open GIF Here", command=browse_file, height=2, width=20, bg='yellow')
open_button.pack(pady=10)

#create the "trim" button (initially red, changes to green when a GIF is selected, then to yellow during processing)
trim_button = tk.Button(button_frame, text="Trim", command=start_process_in_thread, height=2, width=20, bg='red')
trim_button.pack(pady=10)

#create a variable to store the path of the gif when selected (must be defined here)
gif_path = tk.StringVar()

#create the log box at the bottom
log_frame = tk.Frame(root)
log_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
log_box = tk.Text(log_frame, height=10, width=50)
log_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

#add a vertical scrollbar to the log box
scrollbar = tk.Scrollbar(log_frame, command=log_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_box.config(yscrollcommand=scrollbar.set)

#cancel button (initially greyed out, enabled during process)
cancel_button = tk.Button(root, text="Cancel", command=cancel_process, height=2, width=20, bg='yellow', state=tk.DISABLED)
cancel_button.grid(row=2, column=0, columnspan=2, sticky="nsew")

#allow drag and drop of gif files
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop_event)

#start the tkinter event loop
root.mainloop()