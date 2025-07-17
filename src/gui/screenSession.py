from PySide6.QtWidgets import (
    QMainWindow, QLabel, QListWidget
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedLayout
)

import src.gui.widgets as Widgets






class ScreenSession(QWidget):
    def __init__(self):
        super().__init__()
        self.setupGui()

    def setupGui(self):
        label = QLabel("Drop List Widget")
        self.list = Widgets.WidgetListDrop()

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.list)

        self.setLayout(layout)




class WindowSession(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCPR Automation - Session: 00")
        self.resize(600, 400)
        self.screen = ScreenSession()
        self.setCentralWidget(self.screen)