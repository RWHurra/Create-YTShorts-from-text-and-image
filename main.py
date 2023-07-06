import os
import sys
from PyQt6.QtWidgets import (QApplication)
from gui.main_window import MainWindow

# clear previous console prints
os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())