from PySide6.QtWidgets import (
    QLabel, QFrame,
    QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt

import os
import src.gui.widgets as Widgets
import src.gui.style as Style
from src.parser import gui_parser
from src.renamer import gui_indexer


class PanelIndexer(QFrame):
    def __init__(self, _pathInputFolder: str, _pathOutputFolder: str, _pathMoveToFolder: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.pathInputFolder = _pathInputFolder
        self.pathOutputFolder = _pathOutputFolder
        self.pathMoveToFolder = _pathMoveToFolder
        self.pathLogFile = _pathLogFile

        self.widgetTitle = QLabel("File Indexer")
        self.widgetTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        self.widgetInputList = Widgets.ListDragDrop(self.pathInputFolder, (240,240))
        self.widgetInputBtnClear = Widgets.Button(self.widgetInputList.clear_folder, "Clear Folder", (90,30))
        self.widgetInputBtnOpen = Widgets.Button(self.widgetInputList.open_folder, "Open Folder", (90,30))
        self.widgetInputBtnAddFiles = Widgets.Button(self.widgetInputList.add_files, "Add Files", (90,30))
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120,30))
        self.widgetInputField.input.setText(str(1))
        self.widgetInputRun = Widgets.Button(self.indexer, "Run Indexer", (110,30))

        self.widgetOutputList = Widgets.ListDragDrop(self.pathOutputFolder, (240,240))
        self.widgetOutputBtnClear = Widgets.Button(self.widgetOutputList.clear_folder, "Clear Folder", (90,30))
        self.widgetOutputBtnOpen = Widgets.Button(self.widgetOutputList.open_folder, "Open Folder", (90,30))
        self.widgetOutputBtnMove = Widgets.Button(lambda: self.widgetOutputList.move_to_folder(self.pathMoveToFolder), "Move To Parser", (110,30))
     
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
        layoutFrameOutputListButtons.addWidget(self.widgetOutputBtnMove, alignment=Qt.AlignRight)
        layoutFrameOutputList.addLayout(layoutFrameOutputListButtons)
        layoutFrame.addLayout(layoutFrameOutputList)

        layout.addLayout(layoutFrame)
        self.setLayout(layout)


    def indexer(self):
        if not os.path.exists(self.pathInputFolder) or not os.path.exists(self.pathOutputFolder):
            return None
        
        indexStart = self.widgetInputField.input.text().strip()
        indexPrecision = "2"
        if not indexStart.isdigit() or not indexPrecision.isdigit():
            return None
        
        gui_indexer(self.pathInputFolder, self.pathOutputFolder, int(indexStart), int(indexPrecision))



class PanelParser(QFrame):
    def __init__(self, _pathInputFolder: str, _pathOutputFolder: str, _pathMoveToFolder: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.pathInputFolder = _pathInputFolder
        self.pathOutputFolder = _pathOutputFolder
        self.pathMoveToExcelFolder = _pathMoveToFolder / "excel"
        self.pathMoveToJsonFolder = _pathMoveToFolder / "json"
        self.pathLogFile = _pathLogFile

        self.widgetTitle = QLabel("Excel Parser")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        self.widgetInputList = Widgets.ListDragDrop(self.pathInputFolder, (240,240))
        self.widgetInputBtnClear = Widgets.Button(self.widgetInputList.clear_folder, "Clear Folder", (90,30))
        self.widgetInputBtnOpen = Widgets.Button(self.widgetInputList.open_folder, "Open Folder", (90,30))
        self.widgetInputBtnAddFiles = Widgets.Button(self.widgetInputList.add_files, "Add Files", (90,30))
        
        self.widgetInputRun = Widgets.Button(self.parser, "Run Parser", (110,30))

        self.widgetOutputList = Widgets.ListDragDrop(self.pathOutputFolder, (240,240))
        self.widgetOutputBtnClear = Widgets.Button(self.widgetOutputList.clear_folder, "Clear Folder", (90,30))
        self.widgetOutputBtnOpen = Widgets.Button(self.widgetOutputList.open_folder, "Open Folder", (90,30))
        self.widgetOutputBtnMove = Widgets.Button(self.move_input_output, "Move To Session", (110,30))
        
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
        layoutFrameInputConfig.addWidget(self.widgetInputRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutFrameInputConfig.addStretch()
        layoutFrame.addLayout(layoutFrameInputConfig)

        layoutFrameOutputList = QVBoxLayout()
        layoutFrameOutputList.addWidget(self.widgetOutputList)
        layoutFrameOutputListButtons = QHBoxLayout()
        layoutFrameOutputListButtons.addWidget(self.widgetOutputBtnClear, alignment=Qt.AlignLeft)
        layoutFrameOutputListButtons.addStretch()
        layoutFrameOutputListButtons.addWidget(self.widgetOutputBtnOpen)
        layoutFrameOutputListButtons.addWidget(self.widgetOutputBtnMove, alignment=Qt.AlignRight)
        layoutFrameOutputList.addLayout(layoutFrameOutputListButtons)
        layoutFrame.addLayout(layoutFrameOutputList)

        layout.addLayout(layoutFrame)
        self.setLayout(layout)


    def parser(self):
        xlsxList = [file for file in os.listdir(self.pathInputFolder) if file.endswith(".xlsx") or file.endswith(".xlsm")]
        gui_parser(xlsxList, self.pathInputFolder, self.pathOutputFolder, self.pathLogFile)


    def move_input_output(self):
        self.widgetInputList.move_to_folder(self.pathMoveToExcelFolder)
        self.widgetOutputList.move_to_folder(self.pathMoveToJsonFolder)




class ScreenInput(QFrame):
    def __init__(self, _pathIndexer: str, _pathParser, _pathSession, _pathLogFile):
        super().__init__()
        self.pathIndexerInputFolder = _pathIndexer / "input"
        self.pathIndexerOutputFolder = _pathIndexer / "output"
        self.pathParserInputFolder = _pathParser / "input"
        self.pathParserOutputFolder = _pathParser / "output"
        self.pathSessionFolder = _pathSession
        self.pathLogFile = _pathLogFile

        self.setup_ui()


    def setup_ui(self):
        widgetPanelIndexer = PanelIndexer(self.pathIndexerInputFolder, self.pathIndexerOutputFolder, self.pathParserInputFolder, self.pathLogFile)
        widgetPanelParser = PanelParser(self.pathParserInputFolder, self.pathParserOutputFolder, self.pathSessionFolder, self.pathLogFile)

        layout = QVBoxLayout()
        layout.addWidget(widgetPanelIndexer)
        layout.addWidget(widgetPanelParser)

        self.setLayout(layout)