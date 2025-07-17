import os
import re
import sys
import shutil, json
from datetime import datetime


from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QLabel, QListWidget, QPushButton, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit  
)
from PySide6.QtCore import Qt, QFileSystemWatcher
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from src.gui.screenSession import WindowSession


import src.gui.widgets as Widgets
from src.parser import gui_parse_cpr_xlsx_bulk
from src.renamer import gui_bulk_file_index_by_date

styleLabels = """ QLabel {
    font-size: 11pt;
    font-family: 'Segoe UI';
    font-weight: 400;
    }
"""

styleTitle = """ QLabel {
    font-size: 14pt;
    font-family: 'Segoe UI';
    font-weight: 1000;
    }
"""


class PanelIndexer(QWidget):
    def __init__(self, pathFolderList: str, pathFolderNext: str, pathLog: str):
        super().__init__()

        self.widgetTitle = QLabel("File Indexer")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(styleTitle)
        
        self.widgetInputField = Widgets.InputFieldLine("Starting index", (30,30), (120, 30))

        self.pathFolderList = pathFolderList
        self.pathFolderNext = pathFolderNext
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonFolderClear(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetOpen = Widgets.ButtonFolderOpen(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonFolderAddFiles(self.pathFolderList, "Add Files", (90, 30))

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



    
class PanelParser(QWidget):
    def __init__(self, pathFolderList: str, pathFolderNext: str, pathLog: str):
        super().__init__()

        self.widgetTitle = QLabel("Excel Parser")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(styleTitle)

        self.pathFolderList = pathFolderList
        self.pathFolderNext = pathFolderNext
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonFolderClear(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetOpen = Widgets.ButtonFolderOpen(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonFolderAddFiles(self.pathFolderList, "Add Files", (90, 30))

        self.widgetRun = Widgets.Button(self.parser, "Run Parser", (110, 30))
        

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
        layoutConfig.addWidget(self.widgetRun, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutConfig.addStretch()
        layoutFrame.addLayout(layoutConfig)
        layout.addLayout(layoutFrame)

        self.setLayout(layout)

    def parser(self):
        xlsxList = [file for file in os.listdir(self.pathFolderList) if file.endswith(".xlsx") or file.endswith(".xlsm")]
        gui_parse_cpr_xlsx_bulk(xlsxList, self.pathFolderList, self.pathFolderNext, self.pathLog)



class PanelSession(QWidget):
    def __init__(self, pathFolderList: str, pathLog: str):
        super().__init__()

        self.widgetTitle = QLabel("Automation Sessions")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(styleTitle)

        projectTextLabel = "Project DIR:"
        projectTextTemp = "Please type or select Project DIR or Name"
        projectTextList = [
            "",
            "506809 - Sanger Complex III - HARRIS CONSTRUCTION CO INC",
            "506782 - Sanger Aquatics - HARRIS CONSTRUCTION CO INC",
            "496589 - Parlier High - BMY Construction Group, Inc.",
            "493551 - Avenal Tamarack - BMY Construction Group, Inc."
        ]
        self.widgetComboxProject = Widgets.Combox(projectTextLabel, projectTextTemp, projectTextList, (90, 30))

        labelPrime = "Prime:"
        listPrime = [
            "",
            "113061 - HARRIS CONSTRUCTION CO INC",
            "686178 - BMY Construction Group, Inc.",
        ]
        textPrime = "Please type or select Prime ID or Name"
        self.widgetComboxPrime = Widgets.Combox(labelPrime, textPrime, listPrime, (90, 30))

        self.pathFolderList = pathFolderList
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonFolderClear(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetPop = Widgets.ButtonFolderPop(self.pathFolderList, "Delete First", (90, 30))
        self.widgetOpen = Widgets.ButtonFolderOpen(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonFolderAddFiles(self.pathFolderList, "Add Files", (90, 30))

        self.listEntryData = None
        self.entryName = ""
        self.entryProject = ""
        self.entryPrime = ""
    
        self.widgetLoad = Widgets.Button(self.load, "Load", (110, 30))
        self.widgetEntryName = QLabel("Entry: None")
        self.widgetEntryName.setStyleSheet(styleLabels)
        self.widgetEntryProject = QLabel("Project: None")
        self.widgetEntryProject.setStyleSheet(styleLabels)
        self.widgetEntryPrime = QLabel("Prime: None")
        self.widgetEntryPrime.setStyleSheet(styleLabels)


        self.widgetSessionStart = Widgets.Button(self.start, "Start Session", (110, 30))
        

        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)
        layout.addWidget(self.widgetComboxProject)
        layout.addWidget(self.widgetComboxPrime)

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
        layoutConfig.addWidget(self.widgetLoad, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutConfig.addStretch()
        layoutFrame.addLayout(layoutConfig)
        layout.addLayout(layoutFrame)

        layoutSession = QHBoxLayout()

        layoutSessionEntry = QVBoxLayout()
        layoutSessionEntry.addWidget(self.widgetEntryName)
        layoutSessionEntry.addWidget(self.widgetEntryProject)
        layoutSessionEntry.addWidget(self.widgetEntryPrime)
        layoutSession.addLayout(layoutSessionEntry)

        layoutSessionRun = QVBoxLayout()
        layoutSessionRun.addStretch()
        layoutSessionRun.addWidget(self.widgetSessionStart, alignment=Qt.AlignmentFlag.AlignHCenter)
        layoutSessionRun.addStretch()
        layoutSession.addLayout(layoutSessionRun)

        layout.addLayout(layoutSession)

        self.setLayout(layout)

    def load(self):
        if os.path.exists(self.pathFolderList):
            listFolder = sorted(os.listdir(self.pathFolderList))
            if len(listFolder) == 0:
                return None

            self.entryName = listFolder[0]
            self.entryProject = self.widgetComboxProject.combox.currentText().strip()
            self.entryPrime = self.widgetComboxPrime.combox.currentText().strip()

            pathFull = os.path.join(self.pathFolderList, self.entryName)

            self.widgetEntryName.setText(f"Entry: {self.entryName}")
            self.widgetEntryProject.setText(f"Project: {self.entryProject}")
            self.widgetEntryPrime.setText(f"Prime: {self.entryPrime}")

            with open(pathFull, "r", encoding="utf-8") as file:
                self.listEntryData = json.load(file)

    def start(self):
        config = {
            "entry_name": self.entryName,
            "entry_project": self.entryProject,
            "entry_prime": self.entryPrime,
        }

        print(config)




class IndexFilesScreen(QWidget):
    def __init__(self):
        super().__init__()
        pathRoot = Path(__file__).resolve().parents[2]
        pathIndexer = pathRoot / "data" / "indexer"
        pathParser = pathRoot / "data" / "parser"
        pathSession = pathRoot / "data" / "session"
        pathLog = pathRoot / "log"
        timeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.pathFolderIndexer = str(pathIndexer)
        self.pathFolderParser = str(pathParser)
        self.pathFolderSession = str(pathSession)

        os.makedirs(self.pathFolderIndexer, exist_ok=True)
        os.makedirs(self.pathFolderParser, exist_ok=True)
        os.makedirs(self.pathFolderSession, exist_ok=True)
        os.makedirs(pathLog, exist_ok=True)

        self.pathLog = os.path.join(pathLog, f"{timeStamp}.txt")
        with open(self.pathLog, "w", encoding="utf-8") as log:
            log.write(f"### ******************* Log - {timeStamp} ******************* ###\n\n")

        self.windowNext = None
        self.setupUi()


    def setupUi(self):
        self.widgetPanelIndexer = PanelIndexer(self.pathFolderIndexer, self.pathFolderParser, self.pathLog)
        self.widgetPanelParser = PanelParser(self.pathFolderParser, self.pathFolderSession, self.pathLog)
        self.widgetPanelSession = PanelSession(self.pathFolderSession, self.pathLog)

        layout = QVBoxLayout()
        layout.addWidget(self.widgetPanelIndexer)
        layout.addWidget(self.widgetPanelParser)
        layout.addWidget(self.widgetPanelSession)

        self.setLayout(layout)