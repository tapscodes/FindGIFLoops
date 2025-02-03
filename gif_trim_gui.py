import argparse
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image

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

        #compare the current frame with the first frame
        if list(current_frame.getdata()) == list(first_frame.getdata()):
            log_box.insert(tk.END, f"Frame {i+1} is identical to the first frame.\n")
            log_box.yview(tk.END)
            return i + 1  #return the frame number of the duplicate

    log_box.insert(tk.END, "No identical frame found.\n")
    log_box.yview(tk.END)
    return -1  #return -1 if no duplicate was found

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

    #save the new gif
    log_box.insert(tk.END, f"Creating GIF (this can take a while)\n")
    log_box.yview(tk.END)

    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], duration=gif.info['duration'], loop=0)
    log_box.insert(tk.END, f"New GIF created successfully: {output_gif_path}\n")
    log_box.yview(tk.END)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        gif_path.set(file_path)
        log_box.insert(tk.END, f"Selected file: {file_path}\n")
        log_box.yview(tk.END)

def process_gif():
    gif_path_str = gif_path.get()
    if not gif_path_str:
        messagebox.showerror("Error", "No GIF file selected.")
        return

    #find the duplicate frame
    duplicate_frame = find_duplicate_frame(gif_path_str)

    if duplicate_frame == -1:
        messagebox.showinfo("No Duplicate", "No identical frame found. The entire GIF will be used.")
        end_frame = gif.n_frames  #use all frames
    else:
        messagebox.showinfo("Duplicate Found", f"Duplicate found at frame {duplicate_frame}.")
        end_frame = duplicate_frame

    #define the output gif path (same location as input gif)
    output_gif_path = gif_path_str.rsplit('.', 1)[0] + "_trimmed.gif"

    #create the new gif
    create_new_gif(gif_path_str, output_gif_path, end_frame)

    messagebox.showinfo("Process Complete", f"Trimmed GIF created at {output_gif_path}")

def drop_event(event):
    gif_path.set(event.data)
    log_box.insert(tk.END, f"File dropped: {event.data}\n")
    log_box.yview(tk.END)


#tkinter gui setup with drag and drop
root = TkinterDnD.Tk()
root.title("GIF Trim Tool")

#set window size
root.geometry("500x400")

#stringvar to store the file path
gif_path = tk.StringVar()

#create the "open gif here" button
open_button = tk.Button(root, text="Open GIF Here", command=browse_file, height=2, width=20)
open_button.pack(pady=10)

#create the "trim" button
trim_button = tk.Button(root, text="Trim", command=process_gif, height=2, width=20)
trim_button.pack(pady=10)

#create a label for the dropped file path
file_label = tk.Label(root, textvariable=gif_path, wraplength=400)
file_label.pack(pady=10)

#create the log box at the bottom
log_box = tk.Text(root, height=10, width=50)
log_box.pack(pady=20)

#allow drag and drop of gif files
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop_event)

#start the tkinter event loop
root.mainloop()
