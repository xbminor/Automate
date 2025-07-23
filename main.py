import os
import sys
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QFrame, QVBoxLayout

import src.gui.style as Style
from src.gui.screenInput import ScreenInput
from src.gui.screenSession import ScreenSession
from src.gui.screenOutput import ScreenOutput



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCPR Automation")
        self.resize(900, 500)

        pathRoot = Path(__file__).resolve().parents[0]
        pathIndexer = pathRoot / "data" / "indexer"
        pathParser = pathRoot / "data" / "parser"
        pathSession = pathRoot / "data" / "session"
        pathRenamer = pathRoot / "data" / "renamer"
        pathLog = pathRoot / "log"
        timeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        os.makedirs(pathIndexer, exist_ok=True)
        os.makedirs(pathParser, exist_ok=True)
        os.makedirs(pathSession, exist_ok=True)
        os.makedirs(pathRenamer, exist_ok=True)
        os.makedirs(pathLog, exist_ok=True)

        pathLogFile = os.path.join(pathLog, f"{timeStamp}.txt")
        with open(pathLogFile, "w", encoding="utf-8") as log:
            log.write(f"### ******************* Log - {timeStamp} ******************* ###\n\n")

        frameTabs = QFrame()
        frameTabs.setObjectName("TabWrapper")
        frameTabs.setStyleSheet(Style.FRAME_TABS)

        tabs = QTabWidget(frameTabs)
        tabs.setStyleSheet(Style.TABS_DEFAULT)

        tabs.addTab(ScreenInput(pathIndexer, pathParser, pathSession, pathLogFile), "Input")
        tabs.addTab(ScreenSession(pathSession, pathRenamer, pathLogFile), "Session")
        tabs.addTab(ScreenOutput(pathRenamer, pathLogFile), "Output")

        layoutTabs = QVBoxLayout()
        layoutTabs.setContentsMargins(0, 0, 0, 0)
        layoutTabs.addWidget(tabs)
        frameTabs.setLayout(layoutTabs)

        self.setCentralWidget(frameTabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
