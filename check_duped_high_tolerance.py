from PIL import Image
import numpy as np

#open the gif file
gif_path = "predupe.gif"
gif = Image.open(gif_path)

#extract the frames of the gif
frames = []
for frame in range(gif.n_frames):
    gif.seek(frame)  #move to the frame
    frames.append(gif.convert('RGB'))  #convert each frame to rgb

#get the first frame
first_frame = frames[0]
total_frames = len(frames)  #get the total number of frames

#function to compare two frames with tolerance for differences
def frames_are_similar(frame1, frame2, tolerance=0):
    arr1 = np.array(frame1)
    arr2 = np.array(frame2)
    diff = np.abs(arr1 - arr2)  #absolute difference between pixel values
    return np.all(diff <= tolerance)  #check if all pixel differences are within tolerance

#compare each subsequent frame with the first frame
for i, frame in enumerate(frames[1:], start=1):  #start from 1 to compare with first
    print(f"Checking Frame {i+1} / {total_frames}...")  #log the frame being checked
    if frames_are_similar(frame, first_frame, tolerance=5):  #tolerance of 5 for minor differences, going between 5-30 seems to work well
        print(f"Frame {i+1} is identical to the first frame.")
        break
else:
    print("No identical frame found.")
