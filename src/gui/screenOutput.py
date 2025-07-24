from PySide6.QtWidgets import (
    QWidget, QLabel, QFrame,
    QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt

import os
import src.gui.widgets as Widgets
import src.gui.style as Style
from src.renamer import gui_bulk_cpr_index_by_order, gui_bulk_cpr_copy



class PanelRenamer(QFrame):
    def __init__(self, pathFolderList: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.widgetTitle = QLabel("eCPR Renamer")
        self.widgetTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120, 30))

        self.pathFolderList = pathFolderList
        self.pathLogFile = _pathLogFile
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonClearFolder(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetOpen = Widgets.ButtonOpenFolder(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonAddFiles(self.pathFolderList, "Add Files", (90, 30))

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


class PanelNPCopier(QFrame):
    def __init__(self, _pathOutputFolder: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.pathOutputListFolder = _pathOutputFolder
        self.pathLogFile = _pathLogFile

        self.widgetTitle = QLabel("eCPR NP Copier")
        self.widgetTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120, 30))
        self.widgetInputList = Widgets.SingleFileDrop()
        self.widgetInputClear = Widgets.Button(self.widgetInputList.clear_file, "Clear File", (90, 30))
        self.widgetInputAdd = Widgets.Button(self.widgetInputList.add_file, "Add File", (90, 30))
        self.widgetInputRun = Widgets.Button(self.copier, "Run Copier", (110, 30))

        self.widgetOutputList = Widgets.ListDragDrop(self.pathOutputListFolder, 240, 240)
        self.widgetOutputClear = Widgets.ButtonClearFolder(self.pathOutputListFolder, "Clear Folder", (90, 30))
        self.widgetOutputOpen = Widgets.ButtonOpenFolder(self.pathOutputListFolder, "Open Folder", (90, 30))

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)

        layoutInput = QHBoxLayout()
        layoutInputList = QVBoxLayout()
        layoutInputList.addWidget(self.widgetInputList)

        layoutInputListButtons = QHBoxLayout()
        layoutInputListButtons.addWidget(self.widgetInputClear, alignment=Qt.AlignLeft)
        layoutInputListButtons.addWidget(self.widgetInputAdd, alignment=Qt.AlignLeft)
        layoutInputList.addLayout(layoutInputListButtons)
        layoutInput.addLayout(layoutInputList)

        layoutInputConfig = QVBoxLayout()
        layoutInputConfig.addStretch()
        layoutInputConfig.addWidget(self.widgetInputField, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutInputConfig.addWidget(self.widgetInputRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutInputConfig.addStretch()
        layoutInput.addLayout(layoutInputConfig)

        layout.addLayout(layoutInput)


        layoutOutput = QHBoxLayout()
        layoutOutputList = QVBoxLayout()
        layoutOutputList.addWidget(self.widgetOutputList)
        
        layoutResultListButtons = QHBoxLayout()
        layoutResultListButtons.addWidget(self.widgetOutputClear, alignment=Qt.AlignLeft)
        layoutResultListButtons.addStretch()
        layoutResultListButtons.addWidget(self.widgetOutputOpen, alignment=Qt.AlignRight)
        layoutOutputList.addLayout(layoutResultListButtons)
        layoutOutput.addLayout(layoutOutputList)
        layout.addLayout(layoutOutput)

        self.setLayout(layout) 

    def copier(self):
        if os.path.exists(self.pathOutputListFolder):
            text = self.widgetInputField.input.text().strip()
            if not text.isdigit():
                return None
            
            gui_bulk_cpr_copy(self.widgetInputList.get_file(), self.pathOutputListFolder, int(text))


class ScreenOutput(QWidget):
    def __init__(self, _pathRenamer, _pathCopier, _pathLogFile):
        super().__init__()
        self.pathRenamerFolder = _pathRenamer
        self.pathNPCopierFolder = _pathCopier
        self.pathLogFile = _pathLogFile
        self.setupUI()


    def setupUI(self):
        widgetPanelRenamer = PanelRenamer(self.pathRenamerFolder, self.pathLogFile)
        widgetPanelNPCopier = PanelNPCopier(self.pathNPCopierFolder, self.pathLogFile)

        layout = QVBoxLayout()
        layout.addWidget(widgetPanelRenamer)
        layout.addWidget(widgetPanelNPCopier)

        self.setLayout(layout)