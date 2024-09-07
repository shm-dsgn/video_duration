import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QFileDialog,
                             QMessageBox, QProgressDialog, QTreeWidgetItem)
from PyQt6.QtCore import Qt
from drag_drop_tree import DragDropTree
from styles import MAIN_STYLE

class VideoDurationCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Video Duration Calculator")
        self.setGeometry(100, 100, 650, 500)
        self.setStyleSheet(MAIN_STYLE)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        self.file_list = DragDropTree(self, main_window=self)
        self.file_list.setColumnWidth(0, 30)
        self.file_list.setColumnWidth(1, int(self.width() * 0.75))
        layout.addWidget(QLabel("Selected Videos (Drag and Drop here):"))
        layout.addWidget(self.file_list)

        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Add Files")
        add_button.clicked.connect(self.add_videos)
        button_layout.addWidget(add_button)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Playback Speed:"))
        self.speed_input = QLineEdit()
        self.speed_input.setText("1.0")
        speed_layout.addWidget(self.speed_input)
        layout.addLayout(speed_layout)

        calc_button = QPushButton("Calculate Total Duration")
        calc_button.clicked.connect(self.calculate_duration)
        layout.addWidget(calc_button)

        self.result_label = QLabel("Total Duration: ")
        self.result_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.result_label)

        main_widget.setLayout(layout)

    def add_videos(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Videos", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        for file in files:
            self.add_video(file)
    
    def add_video(self, file_path):
        try:
            from moviepy.editor import VideoFileClip
            
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
            item.setToolTip(1, file_path)
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
            from moviepy.editor import VideoFileClip
            
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
                
                file_path = item.toolTip(1)
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
            QMessageBox.warning(self, "Invalid Input", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")