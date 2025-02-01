import argparse
import sys
from PIL import Image

#when you call this file, just input the frame end (the frame you don't want to include found from getting the duplicate) as the paramter (in number form)
def create_new_gif(input_gif_path, output_gif_path, end_frame):
    #open the original gif
    gif = Image.open(input_gif_path)
    
    #total number of frames in the gif
    total_frames = gif.n_frames

    #ensure that the 'end_frame' doesn't exceed the total number of frames
    if end_frame > total_frames:
        print(f"End frame {end_frame} exceeds the total number of frames ({total_frames}).")
        return

    #list to store the frames for the new gif
    frames = []

    #extract frames from the 1st to (end_frame-1)th frame
    for i in range(end_frame - 1):  #go up to the end_frame-1
        gif.seek(i)  #move to the i-th frame
        frames.append(gif.copy())  #append the current frame to the list
        print(f"Trimming Frame {i + 1}...")  #log the frame being processed

    #save the new gif
    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], duration=gif.info['duration'], loop=0)
    print(f"New GIF created successfully: {output_gif_path}")
    
    #explicitly stop the script
    sys.exit()  #ensure the script stops after completion

def main():
    #parse command line arguments
    parser = argparse.ArgumentParser(description="Trim a GIF from frame 1 to a specified frame.")
    parser.add_argument("end_frame", type=int, help="The frame number where the new GIF should end (one frame before this number).")
    args = parser.parse_args()

    #define the input gif and output file paths
    input_gif_path = "predupe.gif"  #input is now fixed to "predupe.gif"
    output_gif_path = "trimmed.gif"  #the output will always be 'trimmed.gif'

    #call the function to create the new gif
    create_new_gif(input_gif_path, output_gif_path, args.end_frame)

if __name__ == "__main__":
    main()
