from PyQt6.QtWidgets import (QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QFileDialog,
                             QTextEdit,
                             QSizePolicy,)
from video_processing.directory_creator import DirectoryCreator
from gui.settings_window import Settings
import settings.default_settings as default_settings
from video_processing.video_creator import VideoCreator

directory_creator = DirectoryCreator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings_window = None  # Initialize the settings window instance variable
        self.setWindowTitle("Create YouTube Shorts")
        self.setGeometry(100, 100, 600, 240)  # Set window's default size

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout(self.central_widget)

        # Buttons container
        button_layout = QVBoxLayout()

        # Set default CSV
        global csv_input
        csv_input = default_settings.DEFAULT_CSV

        # Select CSV button
        self.select_csv_button = QPushButton("✅ Select CSV")
        self.select_csv_button.clicked.connect(self.select_csv)
        button_layout.addWidget(self.select_csv_button)

        # Create Directories button
        self.create_directories_button = QPushButton("📁 Create Directories")
        self.create_directories_button.clicked.connect(self.create_directories)
        button_layout.addWidget(self.create_directories_button)

        # Create Videos button
        self.create_videos_button = QPushButton("▶️ Create Videos")
        self.create_videos_button.clicked.connect(self.create_videos)
        button_layout.addWidget(self.create_videos_button)

        # Create Settings button
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.clicked.connect(self.settings)
        button_layout.addWidget(self.settings_button)

        # Help button
        self.help_button = QPushButton("❓ Help")
        self.help_button.clicked.connect(self.show_help)
        button_layout.addWidget(self.help_button)

        layout.addLayout(button_layout)

        # TextEdit
        self.status_textedit = QTextEdit()
        self.status_textedit.setReadOnly(True)
        layout.addWidget(self.status_textedit)
        global status_textedit
        status_textedit = self.status_textedit

        # Set size policy to expand horizontally and vertically
        self.status_textedit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def get_textedit():
        return status_textedit

    def select_csv(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                global csv_input
                csv_input = selected_files[0]
                self.status_textedit.setPlainText(f"Selected CSV file: {csv_input}")

    def create_directories(self):
        self.status_textedit.setPlainText(f"Creating directories from {csv_input}...")
        directory_creator.create_directories(csv_input, self.status_textedit)

    def create_videos(self):
        self.status_textedit.setPlainText("Creating videos...")
        VideoCreator.scan_directories_and_create_video(self.status_textedit)

    def settings(self):
        self.status_textedit.setPlainText("Opening settings window...")
        if self.settings_window is None:
            self.settings_window = Settings()  # Create the settings window instance
        self.settings_window.show()

    def show_help(self):
        help_message = ("**✅ Select CSV:** Opens a file dialog to select CSV. The CSV must have two columns: setup and punchline. Default CSV is example.csv.\n\n"
            "**📁 Create directories:** Creates directories based on 'setup' from selected CSV. Also creates a text-file in the directory.\n\n"
            "**▶️ Create videos:** Checks all directories if they have a text file and an image (jpg), but no video (mp4). If so, generates videos and places them in the corresponding directory.\n\n"
            "**⚙️ Settings:** Change various settings. Opens in a new window, don't be fooled - press save to save values.\n\n"
            "**❓ Help:** ☝️")

        self.status_textedit.setMarkdown(help_message)