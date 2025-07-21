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

from playwright.sync_api import Playwright, sync_playwright

import src.gui.widgets as Widgets
import src.automate as Automate
from src.parser import gui_parse_cpr_xlsx_bulk
from src.renamer import gui_bulk_file_index_by_date

with open(r".\config.json", "r") as configFile: 
    config = json.load(configFile)

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
        self.widgetPop = Widgets.ButtonFolderPop(self.pathFolderList, "Delete First", (90, 30))
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



class PanelSession(QWidget):
    def __init__(self, pathFolderList: str, pathLog: str):
        super().__init__()

        self.widgetTitle = QLabel("Automation Sessions")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(styleTitle)

        projectTextLabel = "Project DIR:"
        projectTextTemp = "Please type or select Project DIR or Name"
        listTextProject = [
            "",
            "20240559364 - Hawthorne - HARRIS CONSTRUCTION CO INC",
            "506809 - Sanger Complex III - HARRIS CONSTRUCTION CO INC",
            "506782 - Sanger Aquatics - HARRIS CONSTRUCTION CO INC",
            "496589 - Parlier High - BMY Construction Group, Inc.",
            "496574 - Parlier Jr - BMY Construction Group, Inc.",
            "493551 - Avenal Tamarack - BMY Construction Group, Inc.",
        ]
        self.widgetComboxProject = Widgets.Combox(projectTextLabel, projectTextTemp, listTextProject, (90, 30))

        self.pathFolderList = pathFolderList
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonFolderClear(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetPop = Widgets.ButtonFolderPop(self.pathFolderList, "Delete First", (90, 30))
        self.widgetOpen = Widgets.ButtonFolderOpen(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonFolderAddFiles(self.pathFolderList, "Add Files", (90, 30))

        self.listEntryData = None
        self.entryConfig = None
    
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

            fileName = listFolder[0]
            textProject = self.widgetComboxProject.combox.currentText().strip()
            self.entryConfig = config.get(textProject)
            textPrime = self.entryConfig["prime_name"]

            self.widgetEntryName.setText(f"Entry: {fileName}")
            self.widgetEntryProject.setText(f"Project: {textProject}")
            self.widgetEntryPrime.setText(f"Prime: {textPrime}")
            
            pathFull = os.path.join(self.pathFolderList, fileName)

            with open(pathFull, "r", encoding="utf-8") as file:
                self.listEntryData = json.load(file)

    def start(self):
        USERNAME = config["username"]
        PASSWORD = config["password"]
        PROJECT_DIR = self.entryConfig["project"]
        PRIME_ID = self.entryConfig["prime"]
        PRIME_NAME = self.entryConfig["prime_name"]
        CPR_OPEN = config["cpr_open"]
        CPR_ID = config["cpr_id"]

        CPR_NON_WORK = config["cpr_non_work"]


        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(
            viewport={"width":1280, "height":1440},
            # viewport={"width":960, "height":1080},
            # record_video_dir="videos",
            # record_video_size={"width":960, "height":1080}
            )
            page = context.new_page()
            page.goto("https://services.dir.ca.gov/gsp")

            Automate.s0_log_in(page, USERNAME, PASSWORD, self.pathLog)
            Automate.s1_dismiss_announcement(page, self.pathLog)

            if CPR_OPEN:
                Automate.s1_project_dir_cpr_view(page, PROJECT_DIR, self.pathLog)
                Automate.s2_cpr_index_id_open(page, CPR_ID, self.pathLog)
            else:
                Automate.s1_project_dir_cpr_new(page, PROJECT_DIR, self.pathLog)
    
            if CPR_NON_WORK:
                Automate.s3_cpr_fill_non_work(page, PRIME_ID, PRIME_NAME, self.listEntryData, self.pathLog)
            else:
                Automate.s3_cpr_fill(page, PRIME_ID, PRIME_NAME, self.listEntryData, self.pathLog)

            context.close()
            browser.close()




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