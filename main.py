from moviepy.editor import CompositeVideoClip, ImageClip, TextClip, ColorClip
# from moviepy.video.fx import resize
import os

# setup variables
total_duration = 7.0
font_size = 24
font_color = "white"
height_scale = .1
black_bar_scale = 1.4
black_bar_opacity = .6
zoom_factor_start = 2
zoom_factor_end = 1

# find dirs
for dir in os.listdir("."):
    if os.path.isdir(dir):
        print(dir)
        video_name = dir
        print(video_name)

# setup image
image = (ImageClip("test2.jpg")
         .set_duration(total_duration)
         .set_position("center"))
width = image.w
height = image.h

image = image.resize(lambda t: zoom_factor_start + (zoom_factor_end - zoom_factor_start) * t / image.duration)

# setup dad joke
text1 = (TextClip(txt="dad joke setup, but longer. Will this be wrapped?",
                 size=(width, None),
                 fontsize=font_size,
                 color=font_color,
                 method="caption",
                 align="center")
                 .set_position(("center", height_scale*image.h))
                 .set_duration("5.0")
                 .set_start("0.0"))

# setup punchline
text2 = (TextClip(txt="punchline - great! will this also be wrapped?",
                 size=(width, None),
                 fontsize=font_size,
                 color=font_color,
                 method="caption",
                 align="center")
                 .set_position(("center", height_scale*image.h))
                 .set_duration("2.0")
                 .set_start("5.0"))

# setup text background
# Calculate the maximum text height
max_text_height = max(text1.h, text2.h)
black_bar_y = height_scale*image.h - max_text_height*(black_bar_scale - 1)/2

black_bar = (ColorClip(size=(image.w, int(black_bar_scale*max_text_height)),
                      color=(0, 0, 0))
                      .set_opacity(black_bar_opacity)
                      .set_position(("center", black_bar_y))
                      .set_duration(image.duration)
                      .set_start("0.0"))

# create final clip
final_clip = CompositeVideoClip([image, black_bar, text1, text2],
                                size=(width, height))
final_clip = final_clip.write_videofile("composite_clip.mp4", 60)

def CreateTextClip(text, duration):
    text_clip = TextClip(txt=text,
                         size=(.8, 0),
                         color="white").set_duration(duration).set_position(("center", .8), relative=True)
    return text_clip