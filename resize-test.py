from moviepy.editor import CompositeVideoClip, ImageClip, TextClip, ColorClip
from moviepy.video.fx.resize import resize
# CompositeVideoClip, ImageClip, TextClip, ColorClip
# from moviepy.video.fx import resize
import os

# setup variables
total_duration = 7.0
font_size = 200
font_color = "white"
height_scale = .1
black_bar_scale = 1.4
black_bar_opacity = .6
zoom_factor_start = 2
zoom_factor_end = 1

# setup image
image = (ImageClip("test2.jpg")
         .set_position(("center"))
         .set_duration(total_duration))

original_w = image.w
original_h = image.h
image = image.resize(lambda t: zoom_factor_start + (zoom_factor_end - zoom_factor_start) * t / image.duration)
# lambda t:(1 + .001 * t)

#background
background = ColorClip(size=(image.w, image.h),
                       color=(0,0,0)).set_duration(total_duration).set_start(0)

final_clip = CompositeVideoClip([background, image]
                                ,size=(432, 768))

final_clip = final_clip.write_videofile("test-resize.mp4", 12)