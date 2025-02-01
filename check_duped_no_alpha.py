from PIL import Image

#open the GIF file
gif_path = "predupe.gif"
gif = Image.open(gif_path)

#extract the frames of the GIF
frames = []
for frame in range(gif.n_frames):
    gif.seek(frame)  #move to the frame
    frames.append(gif.convert('RGB'))  #convert each frame to RGB, ignoring alpha if present

#get the first frame
first_frame = frames[0]
total_frames = len(frames) #get the total number of frames

#compare each subsequent frame with the first frame
for i, frame in enumerate(frames[1:], start=1):  #start from 1 to compare with first
    print(f"Checking Frame {i+1} / {total_frames}...")  #log the frame being checked
    if list(frame.getdata()) == list(first_frame.getdata()):
        print(f"Frame {i+1} is identical to the first frame.")
        break
else:
    print("No identical frame found.")