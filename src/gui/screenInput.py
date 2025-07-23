from PySide6.QtWidgets import (
    QLabel, QFrame,
    QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt

import os, shutil
import src.gui.widgets as Widgets
import src.gui.style as Style
from src.parser import gui_parse_cpr_xlsx_bulk
from src.renamer import gui_bulk_file_index_by_date


from PySide6.QtGui import QPalette, QColor

class PanelIndexer(QFrame):
    def __init__(self, pathFolderList: str, pathFolderNext: str, pathLog: str):
        super().__init__()

        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.widgetTitle = QLabel("File Indexer")
        self.widgetTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120, 30))
        self.widgetInputField.input.setText(str(1))

        self.pathFolderList = pathFolderList
        self.pathFolderNext = pathFolderNext
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonClearFolder(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetOpen = Widgets.ButtonOpenFolder(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonAddFiles(self.pathFolderList, "Add Files", (90, 30))

        self.widgetRun = Widgets.Button(self.indexer, "Run Indexer", (110, 30))
        self.widgetMove = Widgets.Button(self.move, "Move Files Next", (110, 30))
     


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
        layoutConfig.addWidget(self.widgetMove, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutFrame.addLayout(layoutConfig)

        layout.addLayout(layoutFrame)

        self.setLayout(layout)


    def indexer(self):
        if os.path.exists(self.pathFolderList):
            text = self.widgetInputField.input.text().strip()
            if not text.isdigit():
                return None
            gui_bulk_file_index_by_date(self.pathFolderList, int(text))

    def move(self):
        if not os.path.exists(self.pathFolderList):
            return None
        
        for fileName in os.listdir(self.pathFolderList):
            pathSrc = os.path.join(self.pathFolderList, fileName)
            pathDst = os.path.join(self.pathFolderNext, fileName)
            if os.path.isfile(pathSrc):
                try:
                    shutil.move(pathSrc, pathDst)
                except Exception as e:
                    print(f"Failed to move {fileName}: {e}")



class PanelParser(QFrame):
    def __init__(self, pathFolderList: str, pathFolderNext: str, pathLog: str):
        super().__init__()

        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.widgetTitle = QLabel("Excel Parser")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        self.pathFolderList = pathFolderList
        self.pathFolderNext = pathFolderNext
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonClearFolder(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetPop = Widgets.ButtonPopFolder(self.pathFolderList, "Delete First", (90, 30))
        self.widgetOpen = Widgets.ButtonOpenFolder(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonAddFiles(self.pathFolderList, "Add Files", (90, 30))

        self.widgetRun = Widgets.Button(self.parser, "Run Parser", (110, 30))
        

        layout = QVBoxLayout() 
        layout.addWidget(self.widgetTitle)

        layoutFrame = QHBoxLayout()

        layoutList = QVBoxLayout()
        layoutList.addWidget(self.widgetListFiles)
        
        layoutListButtons = QHBoxLayout()
        layoutListButtons.addWidget(self.widgetClear, alignment=Qt.AlignLeft)
        layoutListButtons.addWidget(self.widgetPop)
        layoutListButtons.addStretch()
        layoutListButtons.addWidget(self.widgetOpen)
        layoutListButtons.addWidget(self.widgetAddFiles, alignment=Qt.AlignRight)
        layoutList.addLayout(layoutListButtons)
        layoutFrame.addLayout(layoutList)

        layoutConfig = QVBoxLayout()
        layoutConfig.addStretch()
        layoutConfig.addWidget(self.widgetRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutConfig.addStretch()
        layoutFrame.addLayout(layoutConfig)
        layout.addLayout(layoutFrame)

        self.setLayout(layout)

    def parser(self):
        xlsxList = [file for file in os.listdir(self.pathFolderList) if file.endswith(".xlsx") or file.endswith(".xlsm")]
        gui_parse_cpr_xlsx_bulk(xlsxList, self.pathFolderList, self.pathFolderNext, self.pathLog)






class ScreenInput(QFrame):
    def __init__(self, _pathIndexer, _pathParser, _pathSession, _pathLogFile):
        super().__init__()
        self.pathIndexerFolder = _pathIndexer
        self.pathParserFolder = _pathParser
        self.pathSessionFolder = _pathSession
        self.pathLogFile = _pathLogFile
        self.setupUI()


    def setupUI(self):
        widgetPanelIndexer = PanelIndexer(self.pathIndexerFolder, self.pathParserFolder, self.pathLogFile)
        widgetPanelParser = PanelParser(self.pathParserFolder, self.pathSessionFolder, self.pathLogFile)

        layout = QVBoxLayout()
        layout.addWidget(widgetPanelIndexer)
        layout.addWidget(widgetPanelParser)

        self.setLayout(layout)