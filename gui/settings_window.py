from PyQt6.QtWidgets import (QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QLabel,
                             QLineEdit,
                             QPushButton)
import settings.default_settings as default_settings

class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        
        # Create the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Create the layout
        layout = QVBoxLayout(self.central_widget)
        global initial_settings
        initial_settings = default_settings.SETTINGS

        # Create labels and line edits for each setting from default settings
        self.line_edits = {}
        for key, value in initial_settings.items():
            # Create label
            label_widget = QLabel(key)
            layout.addWidget(label_widget)

            # Create the line edit and set the default value
            line_edit = QLineEdit(str(value))
            self.line_edits[key] = line_edit
            layout.addWidget(line_edit)

        self.save_button = QPushButton("💾 Save")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

    def save_changes(self):
        for key, value in self.line_edits.items():
            initial_settings[key] = value.text()
        self.close()
        
    def get_settings(self):
        # Retrieve the values from the line edits and return as a dictionary
        settings = {}
        for label, line_edit in self.line_edits.items():
            settings[label] = line_edit.text()
        return settings