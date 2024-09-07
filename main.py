import sys
from PyQt6.QtWidgets import QApplication
from video_duration_calculator import VideoDurationCalculator

def main():
    app = QApplication(sys.argv)
    window = VideoDurationCalculator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()