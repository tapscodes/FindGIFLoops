# GIF Frame Duplicate Scripts
check when the first duplicate frame in a GIF is
## Requirements
1. Install Python from https://www.python.org/
2. Run the command ```pip install pillow imagehash``` to install imagehash and pillow
3. Put your gif in the same folder as check_duped_frame.py and call it "predupe.gif"
4. Run the script by pasting ```python check_duped_no_alpha_no_async.py``` in the terminal (or python3 if on mac)
5. Run the trimming script by pasting ```python trim_gif.py (frame number)``` with the frame number given by the previous script to create a trimmed looping version of the input gif.
## Alternate Scripts [no alpha no async is GENERALLY best, high tolerance is FASTEST]
- check_duped_frame.py finds first perfect match to first frame of GIF (if any), to make a loop simply delete that frame and every one after it.
- check_duped_no_alpha.py ignores the alpha value as it often isn't needed and slight differences can throw off the program finding a pixel-perfect match.
- check_duped_high_tolerance.py has a higher tolerance for minor differnces that a human eye might not catch, however won't be perfect.
- check_dupes_no_alpha_no_async.py is the same as no_alpha but it doesn't do it at the same time. use this if your gif is large (such as the 4GB one I tested on)
## Output
- Checking Frame x/y... means that frame x is currently being compared to the first frame of a total of y frames. This can take some time depending on the image size of each frame of the GIF.
- Frame _ is identical to the first frame means exactly what it says. To make a looping gif from here, simply use frame 1 to the frame before that one.
- No identical frame found. means that the program didn't find any identical frames with the current parameters, you might want to consider one of the alternate scripts availabe if you do bleieve it loops.