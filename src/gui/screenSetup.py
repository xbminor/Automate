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