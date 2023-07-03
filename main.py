from moviepy.editor import CompositeVideoClip, ImageClip, TextClip, ColorClip
# from moviepy.video.fx import resize
import os
import csv
import wx

# setup variables
fps = 12
total_duration = 7.0
font_size = 24
font_color = "white"
height_scale = .1
black_bar_scale = 1.4
black_bar_opacity = .6
zoom_factor_start = 2
zoom_factor_end = 1
csv_input = "dad-jokes.csv"

# definitions
# --------------------------------------
# create folders from CSV-file
def CreateDirectories(csv_file):
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Extract joke details from the CSV row
            setup = row["Setup"]
            punchline = row["Punchline"]
            os.makedirs(setup.rstrip('?'), exist_ok=True)

def SetupImage(image_filepath):
    image = (ImageClip(image_filepath)
         .set_duration(total_duration)
         .set_position("center"))
    global width, height
    width = image.w
    height = image.h
    image = image.resize(lambda t: zoom_factor_start + (zoom_factor_end - zoom_factor_start) * t / image.duration)
    return image
    print("Image setup!")

def SetupJoke(joke_filepath):
    # setup joke
    text1 = (TextClip(txt="dad joke setup, but longer. Will this be wrapped?", # TODO: get text from .TXT
                 size=(width, None),
                 fontsize=font_size,
                 color=font_color,
                 method="caption",
                 align="center")
                 .set_position(("center", height_scale*image.h))
                 .set_duration("5.0")
                 .set_start("0.0"))

    # setup punchline
    text2 = (TextClip(txt="punchline - great! will this also be wrapped?", # TODO: get text from .TXT
                 size=(width, None),
                 fontsize=font_size,
                 color=font_color,
                 method="caption",
                 align="center")
                 .set_position(("center", height_scale*image.h))
                 .set_duration("2.0")
                 .set_start("5.0"))
    return text1, text2

def CreateVideo(setup, punchline, image, directory):
    max_text_height = max(setup.h, punchline.h)
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
    print(setup.txt)
    final_clip = final_clip.write_videofile(directory + "/" + directory + ".mp4", fps)

def CheckVideoReadiness(dir):
    for file in os.listdir("./" + dir):
        print("\tFound file: \t", file)
        file_extension = os.path.splitext(file)[1]
        if file_extension == ".txt":
            contains_joke = True
        if file_extension == ".jpg":
            contains_image = True
        if file_extension == ".mp4":
            contains_video = True               
        print("\tContains joke: \t", contains_joke)
        print("\tContains img: \t", contains_image)
        print("\tContains vid: \t", contains_video)
        if contains_joke == True and contains_image == True and contains_video == False:
            is_ready = True
        if is_ready == True:
            print("------> ", dir, " is ready for video!")
        else:
            print("------> ", dir, " is __NOT__ ready for video!")
        return is_ready

# create dirs
CreateDirectories(csv_input)

# find dirs ready for video
for dir in os.listdir("."):
    contains_joke = False
    joke_filepath = "path"
    contains_image = False
    image_filepath = "path"
    contains_video = False
    is_ready = False
    if os.path.isdir(dir) and dir != ".git":
        print("Found directory: ", dir)
        video_name = dir
        for file in os.listdir("./" + dir):
            print("\tFound file: \t", file)
            file_extension = os.path.splitext(file)[1]
            if file_extension == ".txt":
                contains_joke = True
                joke_filepath = file
            if file_extension == ".jpg":
                contains_image = True
                image_filepath = file
            if file_extension == ".mp4":
                contains_video = True               
        print("\tContains joke: \t", contains_joke)
        print("\tContains img: \t", contains_image)
        print("\tContains vid: \t", contains_video)
        if contains_joke == True and contains_image == True and contains_video == False:
            is_ready = True
        if is_ready == True:
            print("------> ", dir, " is ready for video!")
            image = SetupImage(image_filepath)
            text1, text2 = SetupJoke(joke_filepath)
            CreateVideo(text1, text2, image, dir)

        else:
            print("------> ", dir, " is __NOT__ ready for video!")

# test GUI
class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Create Youtube shorts')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL) 
        # self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5))
        # my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        button_create_dirs = wx.Button(panel, label='Create directories', pos=(5, 55))
        button_select_CSV = wx.Button(panel, label='Select CSV', pos=(5, 55))
        button_create_dirs.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(button_create_dirs, 0, wx.ALL | wx.CENTER, 10)        
        my_sizer.Add(button_select_CSV, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)

        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

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
# final_clip = final_clip.write_videofile("composite_clip.mp4", 12)

def CreateTextClip(text, duration):
    text_clip = TextClip(txt=text,
                         size=(.8, 0),
                         color="white").set_duration(duration).set_position(("center", .8), relative=True)
    return text_clip