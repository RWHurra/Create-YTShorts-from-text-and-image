from moviepy.editor import (CompositeVideoClip,
                            ImageClip,
                            TextClip,
                            ColorClip)
import os
import settings.default_settings as default_settings

class VideoCreator():
    # =================
    # GET SETTINGS
    # =================
    global settings
    settings = default_settings.SETTINGS

    # =================
    # SETUP IMAGE
    # =================
    def setup_image(image_filepath):
        print(settings.items())
        print("settings['TOTAL_DURATION']: " + str(settings['TOTAL_DURATION']))
        print("settings['FPS']: " + str(settings['FPS']))
        global image
        image = (ImageClip(image_filepath)
            .set_duration(float(settings['TOTAL_DURATION']))
            .set_position("center"))
        global width, height
        width = image.w
        height = image.h
        image = (image.resize(lambda t: int(settings['ZOOM_FACTOR_START'])
                              + (int(settings['ZOOM_FACTOR_END']) - int(settings['ZOOM_FACTOR_START'])) * t
                              / image.duration))
        return image

    # =================
    # SETUP JOKE
    # =================
    def setup_joke(joke_filepath):
        # read txt
        with open(joke_filepath, "r") as filestream:
            for line in filestream:
                currentline = line.split(",")
                setup = currentline[0].replace('"', '')
                punchline = currentline[1].replace('"', '')
        # setup joke
        global text1, text2
        text1 = (TextClip(txt=setup,
                    size=(width, None),
                    fontsize=int(settings['FONT_SIZE']),
                    color=settings['FONT_COLOR'],
                    method="caption",
                    align="center")
                    .set_position(("center", float(settings['HEIGHT_SCALE']) * image.h))
                    .set_duration("5.0")
                    .set_start("0.0"))

        # setup punchline
        text2 = (TextClip(txt=punchline,
                    size=(width, None),
                    fontsize=int(settings['FONT_SIZE']),
                    color=settings['FONT_COLOR'],
                    method="caption",
                    align="center")
                    .set_position(("center", float(settings['HEIGHT_SCALE']) * image.h))
                    .set_duration("2.0")
                    .set_start("5.0"))
        return text1, text2

    # =================
    # CREATE VIDEO
    # =================
    def create_video(setup, punchline, image, directory):
        max_text_height = max(setup.h, punchline.h)
        black_bar_y = float(settings['HEIGHT_SCALE']) * image.h - max_text_height * (float(settings['BLACK_BAR_SCALE']) - 1)/2

        black_bar = (ColorClip(size=(image.w, int(float(settings['BLACK_BAR_SCALE']) * max_text_height)),
                            color=(0, 0, 0))
                            .set_opacity(float(settings['BLACK_BAR_OPACITY']))
                            .set_position(("center", black_bar_y))
                            .set_duration(image.duration)
                            .set_start("0.0"))

        # create final clip
        final_clip = CompositeVideoClip([image, black_bar, text1, text2],
                                        size=(width, height))
        final_clip = final_clip.write_videofile(directory + "/" + directory + ".mp4", fps=int(settings['FPS']))

    # =================
    # SCAN DIRECTORIES AND CREATE VIDEO -> REFACTOR?
    # =================
    def scan_directories_and_create_video(status_textedit):
        created_video = False
        count_missing_image = 0
        string_missing_image = ""
        for dir in os.listdir("."):
            contains_joke = False
            joke_filepath = "path"
            contains_image = False
            image_filepath = "path"
            contains_video = False
            is_ready = False
            if os.path.isdir(dir) and dir != ".git":
                print("Found directory: ", dir)
                for file in os.listdir("./" + dir):
                    print("\tFound file: \t", file)
                    file_extension = os.path.splitext(file)[1]
                    if file_extension == ".txt":
                        contains_joke = True
                        joke_filepath = dir + "/" + file
                    if file_extension == ".jpg":
                        contains_image = True
                        image_filepath = file
                    if file_extension == ".mp4":
                        contains_video = True               
                print("\tContains joke: \t", contains_joke)
                print("\tContains img: \t", contains_image)
                print("\tContains vid: \t", contains_video)
                if contains_image == False:
                    count_missing_image += 1
                    string_missing_image += dir + "\n"
                if contains_joke == True and contains_image == True and contains_video == False:
                    is_ready = True
                if is_ready == True:
                    print("------> ", dir, " is ready for video!")
                    image = VideoCreator.setup_image(image_filepath)
                    text1, text2 = VideoCreator.setup_joke(joke_filepath)
                    VideoCreator.create_video(text1, text2, image, dir)
                    status_textedit.append("Created video: " + dir)
                    created_video = True
                else:
                    print("------> ", dir, " is __NOT__ ready for video!")
        if created_video == False:
            status_textedit.append("Found no directory ready for video...")
            status_textedit.append(str(count_missing_image) + " directories have missing images:")
            status_textedit.append(string_missing_image)