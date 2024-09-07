from PyQt6.QtWidgets import QTreeWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from styles import TREE_STYLE

class DragDropTree(QTreeWidget):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.setAcceptDrops(True)
        self.setColumnCount(3)
        self.setHeaderLabels(["", "File Name", "Duration"])
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setIndentation(0)
        self.setStyleSheet(TREE_STYLE)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if self.main_window and hasattr(self.main_window, 'add_video'):
                    self.main_window.add_video(file_path)
        else:
            event.ignore()