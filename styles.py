MAIN_STYLE = """
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
    background-color: #4b6ca3;
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
"""

TREE_STYLE = """
QTreeWidget::item {
    padding: 2px 5px;
}
QTreeWidget::indicator {
    padding-left: 5px;
}
"""