# CreateYTShorts
 Simple application to automate the process to create Youtube-shorts based on text and image.

 This script will load a CSV containing two part dad jokes.

 The setup (part one) of the dad joke will be used to create directories.

 There is an loop to check if a dicetory is ready to generate a video. A directory is ready if:
 - there is a .TXT containing the dad joke
 - there is an image to use as background
 - there is NO video

To generate the video MoviePy is used.
The .TXT must be two-parts, a setup for the dad joke and a punchline.
The image will be used as background, starting at 2x-zoom, ending at 1x-zoom.
A black-bar will be added below the text to make the text more readible.

At the beginning of the script relevant variables can be changed.
