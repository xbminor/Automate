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
    def __init__(self, _pathInputFolder: str, _pathOutputFolder: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.pathInputFolder = _pathInputFolder
        self.pathOutputFolder = _pathOutputFolder
        self.pathLogFile = _pathLogFile

        self.widgetTitle = QLabel("eCPR Renamer")
        self.widgetTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        self.widgetInputList = Widgets.ListDragDrop(self.pathInputFolder, (240,240))
        self.widgetInputBtnClear = Widgets.Button(self.widgetInputList.clear_folder, "Clear Folder", (90,30))
        self.widgetInputBtnOpen = Widgets.Button(self.widgetInputList.open_folder, "Open Folder", (90,30))
        self.widgetInputBtnAddFiles = Widgets.Button(self.widgetInputList.add_files, "Add Files", (90,30))
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120,30))
        self.widgetInputField.input.setText(str(1))
        self.widgetInputRun = Widgets.Button(self.renamer, "Run Renamer", (110,30))
        
        self.widgetOutputList = Widgets.ListDragDrop(self.pathOutputFolder, (240,240))
        self.widgetOutputBtnClear = Widgets.Button(self.widgetOutputList.clear_folder, "Clear Folder", (90,30))
        self.widgetOutputBtnOpen = Widgets.Button(self.widgetOutputList.open_folder, "Open Folder", (90,30))

        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)

        layoutFrame = QHBoxLayout()

        layoutFrameInputList = QVBoxLayout()
        layoutFrameInputList.addWidget(self.widgetInputList)
        layoutFrameInputListButtons = QHBoxLayout()
        layoutFrameInputListButtons.addWidget(self.widgetInputBtnClear, alignment=Qt.AlignLeft)
        layoutFrameInputListButtons.addStretch()
        layoutFrameInputListButtons.addWidget(self.widgetInputBtnOpen)
        layoutFrameInputListButtons.addWidget(self.widgetInputBtnAddFiles, alignment=Qt.AlignRight)
        layoutFrameInputList.addLayout(layoutFrameInputListButtons)
        layoutFrame.addLayout(layoutFrameInputList)

        layoutFrameInputConfig = QVBoxLayout()
        layoutFrameInputConfig.addStretch()
        layoutFrameInputConfig.addWidget(self.widgetInputField, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutFrameInputConfig.addWidget(self.widgetInputRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutFrameInputConfig.addStretch()
        layoutFrame.addLayout(layoutFrameInputConfig)

        layoutFrameOutputList = QVBoxLayout()
        layoutFrameOutputList.addWidget(self.widgetOutputList)
        layoutFrameOutputListButtons = QHBoxLayout()
        layoutFrameOutputListButtons.addWidget(self.widgetOutputBtnClear, alignment=Qt.AlignLeft)
        layoutFrameOutputListButtons.addStretch()
        layoutFrameOutputListButtons.addWidget(self.widgetOutputBtnOpen)
        layoutFrameOutputList.addLayout(layoutFrameOutputListButtons)
        layoutFrame.addLayout(layoutFrameOutputList)

        layout.addLayout(layoutFrame)
        self.setLayout(layout)


    def renamer(self):
        if os.path.exists(self.pathInputFolder):
            text = self.widgetInputField.input.text().strip()
            if not text.isdigit():
                return None
            gui_bulk_cpr_index_by_order(self.pathInputFolder, int(text))



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
        
        self.widgetInputList = Widgets.SingleFileDrop()
        self.widgetInputBtnClear = Widgets.Button(self.widgetInputList.clear_file, "Clear File", (90,30))
        self.widgetInputBtnAdd = Widgets.Button(self.widgetInputList.add_file, "Add File", (90,30))
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120,30))
        self.widgetInputBtnRun = Widgets.Button(self.copier, "Run Copier", (110,30))

        self.widgetOutputList = Widgets.ListDragDrop(self.pathOutputListFolder, (240, 240))
        self.widgetOutputBtnClear = Widgets.Button(self.widgetOutputList.clear_folder, "Clear Folder", (90,30))
        self.widgetOutputBtnOpen = Widgets.Button(self.widgetOutputList.open_folder, "Open Folder", (90,30))

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)

        layoutInput = QHBoxLayout()

        layoutInputList = QVBoxLayout()
        layoutInputList.addWidget(self.widgetInputList)
        layoutInputListButtons = QHBoxLayout()
        layoutInputListButtons.addWidget(self.widgetInputBtnClear, alignment=Qt.AlignLeft)
        layoutInputListButtons.addWidget(self.widgetInputBtnAdd, alignment=Qt.AlignLeft)
        layoutInputList.addLayout(layoutInputListButtons)
        layoutInput.addLayout(layoutInputList)

        layoutInputConfig = QVBoxLayout()
        layoutInputConfig.addStretch()
        layoutInputConfig.addWidget(self.widgetInputField, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutInputConfig.addWidget(self.widgetInputBtnRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutInputConfig.addStretch()
        layoutInput.addLayout(layoutInputConfig)
        layout.addLayout(layoutInput)

        layoutOutput = QHBoxLayout()
        layoutOutputList = QVBoxLayout()
        layoutOutputList.addWidget(self.widgetOutputList)
        
        layoutResultListButtons = QHBoxLayout()
        layoutResultListButtons.addWidget(self.widgetOutputBtnClear, alignment=Qt.AlignLeft)
        layoutResultListButtons.addStretch()
        layoutResultListButtons.addWidget(self.widgetOutputBtnOpen, alignment=Qt.AlignRight)
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
        self.pathRenamerInputFolder = _pathRenamer / "input"
        self.pathRenamerOutputFolder = _pathRenamer / "output"
        self.pathNPCopierFolder = _pathCopier
        self.pathLogFile = _pathLogFile
        self.setupUI()


    def setupUI(self):
        widgetPanelRenamer = PanelRenamer(self.pathRenamerInputFolder, self.pathRenamerOutputFolder, self.pathLogFile)
        widgetPanelNPCopier = PanelNPCopier(self.pathNPCopierFolder, self.pathLogFile)

        layout = QVBoxLayout()
        layout.addWidget(widgetPanelRenamer)
        layout.addWidget(widgetPanelNPCopier)

        self.setLayout(layout)