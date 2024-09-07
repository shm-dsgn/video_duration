import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QFileDialog, QStyle,
                             QMessageBox, QProgressDialog, QTreeWidget, QTreeWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from moviepy.editor import VideoFileClip

class DragDropTree(QTreeWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAcceptDrops(True)
        self.setColumnCount(3)
        self.setHeaderLabels(["", "File Name", "Duration"])
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setIndentation(0)  # Remove indentation
        self.setStyleSheet("""
            QTreeWidget::item {
                padding-left: 5px;
                padding-right: 5px;
                padding-top: 2px;
                padding-bottom: 2px;
            }
            QTreeWidget::indicator {
                padding-left: 5px;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    if self.main_window and hasattr(self.main_window, 'add_video'):
                        self.main_window.add_video(file_path)
                    else:
                        print("Error: main_window not set or add_video method not found")
        else:
            if event.source() == self:
                event.setDropAction(Qt.DropAction.MoveAction)
                super().dropEvent(event)
            else:
                event.ignore()

class VideoDurationCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        # TODO: Add Icon
        self.setWindowTitle("Video Duration Calculator")
        self.setGeometry(100, 100, 650, 500)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #121212;
            }
            QLabel {
                font-size: 12px;
                margin-bottom: 5px;
            }
            QPushButton {
                background-color: #567dbf;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2e4266;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #757575;
                background-color: #3b3b3b;
                color: #ffffff;
                border-radius: 8px;
            }
            QTreeWidget {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #3b3b3b;
                color: #ffffff;
            }
            QTreeWidget::item:selected {
                background-color: #555;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #555;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # File list
        self.file_list = DragDropTree(self, main_window=self)
        self.file_list.setColumnWidth(0, 30)
        self.file_list.setColumnWidth(1, int(self.width() * 0.75))
        layout.addWidget(QLabel("Selected Videos (Drag and Drop here):"))
        layout.addWidget(self.file_list)

        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Add files button
        add_button = QPushButton("Add Files")
        add_button.clicked.connect(self.add_videos)
        button_layout.addWidget(add_button)

        # Remove selected button
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        # Playback speed input
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Playback Speed:"))
        self.speed_input = QLineEdit()
        self.speed_input.setText("1.0")
        speed_layout.addWidget(self.speed_input)
        layout.addLayout(speed_layout)

        # Calculate button
        calc_button = QPushButton("Calculate Total Duration")
        calc_button.clicked.connect(self.calculate_duration)
        layout.addWidget(calc_button)
        # layout.addWidget(self.calc_button)

        # Result display
        self.result_label = QLabel("Total Duration: ")
        # self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.result_label)

        main_widget.setLayout(layout)

    def add_videos(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Videos", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        for file in files:
            self.add_video(file)
    
    def add_video(self, file_path):
        try:
            clip = VideoFileClip(file_path)
            duration = clip.duration
            clip.close()
            
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            
            item = QTreeWidgetItem(self.file_list)
            item.setCheckState(0, Qt.CheckState.Unchecked)
            item.setText(1, os.path.basename(file_path))
            item.setText(2, duration_str)
            item.setToolTip(1, file_path) # Set the full path as a tooltip
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not process file: {file_path}\nError: {str(e)}")
    
    def remove_selected(self):
        root = self.file_list.invisibleRootItem()
        for item in self.get_all_items():
            if item.checkState(0) == Qt.CheckState.Checked:
                (item.parent() or root).removeChild(item)
    
    def get_all_items(self):
        all_items = []
        for i in range(self.file_list.topLevelItemCount()):
            all_items.extend(self.get_subtree_nodes(self.file_list.topLevelItem(i)))
        return all_items
    
    def get_subtree_nodes(self, item):
        nodes = [item]
        for i in range(item.childCount()):
            nodes.extend(self.get_subtree_nodes(item.child(i)))
        return nodes

    def calculate_duration(self):
        try:
            total_duration = 0
            speed = float(self.speed_input.text())
            if speed <= 0:
                raise ValueError("Playback speed must be a positive number")

            all_items = self.get_all_items()
            progress = QProgressDialog("Calculating duration...", "Cancel", 0, len(all_items), self)
            progress.setWindowModality(Qt.WindowModality.WindowModal)

            for i, item in enumerate(all_items):
                if progress.wasCanceled():
                    break
                progress.setValue(i)
                
                file_path = item.toolTip(1)  # Get the full path from the tooltip
                try:
                    clip = VideoFileClip(file_path)
                    duration = clip.duration
                    total_duration += duration
                    clip.close()
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not process file: {file_path}\nError: {str(e)}")

            progress.setValue(len(all_items))

            adjusted_duration = total_duration / speed
            hours, remainder = divmod(adjusted_duration, 3600)
            minutes, seconds = divmod(remainder, 60)

            result = f"Total Duration: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            self.result_label.setText(result)
        except ValueError as e:
            self.debug_label.setText(f"Debug Info: ValueError - {str(e)}")
            QMessageBox.warning(self, "Invalid Input", str(e))
        except Exception as e:
            self.debug_label.setText(f"Debug Info: Unexpected error - {str(e)}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoDurationCalculator()
    window.show()
    sys.exit(app.exec())