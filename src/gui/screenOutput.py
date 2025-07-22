from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt

import os
import src.gui.widgets as Widgets
from src.renamer import gui_bulk_cpr_index_by_order

styleLabels = """ QLabel {
    font-size: 11pt;
    font-family: 'Segoe UI';
    font-weight: 400;
    }
"""

styleTitle = """ QLabel {
    font-size: 14pt;
    font-family: 'Segoe UI';
    font-weight: 1000;W
    }
"""



class PanelRenamer(QWidget):
    def __init__(self, pathFolderList: str, pathLogFile: str):
        super().__init__()

        self.widgetTitle = QLabel("eCPR Renamer")
        self.widgetTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgetTitle.setStyleSheet(styleTitle)
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120, 30))

        self.pathFolderList = pathFolderList
        self.pathLog = pathLogFile
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonFolderClear(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetOpen = Widgets.ButtonFolderOpen(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonFolderAddFiles(self.pathFolderList, "Add Files", (90, 30))

        self.widgetRun = Widgets.Button(self.renamer, "Run Renamer", (110, 30))
     


        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)

        layoutFrame = QHBoxLayout()

        layoutList = QVBoxLayout()
        layoutList.addWidget(self.widgetListFiles)
        
        layoutListButtons = QHBoxLayout()
        layoutListButtons.addWidget(self.widgetClear, alignment=Qt.AlignLeft)
        layoutListButtons.addStretch()
        layoutListButtons.addWidget(self.widgetOpen)
        layoutListButtons.addWidget(self.widgetAddFiles, alignment=Qt.AlignRight)
        layoutList.addLayout(layoutListButtons)
        layoutFrame.addLayout(layoutList)

        layoutConfig = QVBoxLayout()
        layoutConfig.addStretch()
        layoutConfig.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layoutConfig.addWidget(self.widgetInputField, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutConfig.addWidget(self.widgetRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutConfig.addStretch()

        layoutFrame.addLayout(layoutConfig)

        layout.addLayout(layoutFrame)

        self.setLayout(layout) 

    def renamer(self):
        if os.path.exists(self.pathFolderList):
            text = self.widgetInputField.input.text().strip()
            if not text.isdigit():
                return None
            gui_bulk_cpr_index_by_order(self.pathFolderList, int(text))


class ScreenOutput(QWidget):
    def __init__(self, _pathRenamer, _pathLogFile):
        super().__init__()
        self.pathRenamerFolder = _pathRenamer
        self.pathLogFile = _pathLogFile
        self.setupUI()


    def setupUI(self):
        widgetPanelRenamer = PanelRenamer(self.pathRenamerFolder, self.pathLogFile)

        layout = QVBoxLayout()
        layout.addWidget(widgetPanelRenamer)

        self.setLayout(layout)