from moviepy.editor import CompositeVideoClip, ImageClip, TextClip, ColorClip
import os
import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QSizePolicy
# import wx

# clear previous console prints
os.system('cls' if os.name == 'nt' else 'clear')

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
            with open(setup.rstrip('?') + '/' + 'dad-joke.txt', 'w') as f:
                f.write('"' + setup + '", "' + punchline + '"')

def SetupImage(image_filepath):
    global image
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
    with open(joke_filepath, "r") as filestream:
        for line in filestream:
            currentline = line.split(",")
            setup = currentline[0].replace('"', '')
            punchline = currentline[1].replace('"', '')
    global text1, text2
    text1 = (TextClip(txt=setup, # TODO: get text from .TXT
                 size=(width, None),
                 fontsize=font_size,
                 color=font_color,
                 method="caption",
                 align="center")
                 .set_position(("center", height_scale*image.h))
                 .set_duration("5.0")
                 .set_start("0.0"))

    # setup punchline
    text2 = (TextClip(txt=punchline, # TODO: get text from .TXT
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

def ScanDirectoriesCreateVideo():
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
                    joke_filepath = dir + "/" + file
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



# # test GUI
# Subclass QMainWindow to customize your application's main window


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create YouTube Shorts")
        self.setGeometry(100, 100, 600, 240)  # Set window's default size

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout(self.central_widget)

        # Buttons container
        button_layout = QVBoxLayout()

        # Select CSV button
        self.select_csv_button = QPushButton("Select CSV")
        self.select_csv_button.clicked.connect(self.select_csv)
        button_layout.addWidget(self.select_csv_button)

        # Create Directories button
        self.create_directories_button = QPushButton("Create Directories")
        self.create_directories_button.clicked.connect(self.create_directories)
        button_layout.addWidget(self.create_directories_button)

        # Create Videos button
        self.create_videos_button = QPushButton("Create Videos")
        self.create_videos_button.clicked.connect(self.create_videos)
        button_layout.addWidget(self.create_videos_button)

        # Help button
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)
        button_layout.addWidget(self.help_button)

        layout.addLayout(button_layout)

        # TextEdit
        self.status_textedit = QTextEdit()
        self.status_textedit.setReadOnly(True)
        layout.addWidget(self.status_textedit)

        # Set size policy to expand horizontally and vertically
        self.status_textedit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def select_csv(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                csv_input = selected_files[0]
                self.status_textedit.setPlainText(f"Selected CSV file: {csv_input}")

    def create_directories(self):
        self.status_textedit.setPlainText(f"Creating directories from {csv_input}...")
        CreateDirectories(csv_input)

    def create_videos(self):
        ScanDirectoriesCreateVideo()
        self.status_textedit.setPlainText("Creating videos...")

    def show_help(self):
        # Show help message or open help dialog here
        self.status_textedit.setPlainText(
            "Select CSV: Opens a file dialog to select CSV. The CSV must have two columns: setup and punchline.\n\n"
            "Create directories: Creates directories based on 'setup' from selected CSV. Also creates a text-file in the directory.\n\n"
            "Create videos: Checks all directories if they have a text file and an image (jpg), but no video (mp4). If so, generates videos and places them in the corresponding directory."
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())