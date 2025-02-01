from PIL import Image

#open the gif file
gif_path = "predupe.gif"
gif = Image.open(gif_path)

#get the first frame
gif.seek(0)  #move to the first frame
first_frame = gif.convert('RGB')  #convert the first frame to rgb

#total number of frames in the gif
total_frames = gif.n_frames

#compare each subsequent frame with the first frame
for i in range(1, total_frames):  #start from the second frame
    gif.seek(i)  # move to the i-th frame
    current_frame = gif.convert('RGB')  #convert the current frame to rgb
    
    print(f"Checking Frame {i+1} / {total_frames}...")  #log the frame being checked
    
    # compare the current frame with the first frame
    if list(current_frame.getdata()) == list(first_frame.getdata()):
        print(f"Frame {i+1} is identical to the first frame.")
        break
else:
    print("No identical frame found.")