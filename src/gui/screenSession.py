from PySide6.QtWidgets import (
    QWidget, QLabel, QFrame,
    QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt, Signal, QFileSystemWatcher
from playwright.sync_api import sync_playwright

import os, json, subprocess, time

import src.gui.widgets as Widgets
import src.gui.style as Style
import src.automate as Automate

with open(r".\config.json", "r") as configFile: 
    config = json.load(configFile)



class PanelSetup(QFrame):
    signalProjectSelected = Signal(list)

    def __init__(self, _pathExcelFolder: str, _pathJsonFolder: str, _pathInputFolder: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.pathExcelFolder = _pathExcelFolder
        self.pathJsonFolder = _pathJsonFolder
        self.pathInputFolder = _pathInputFolder
        self.pathLogFile = _pathLogFile
        self.pathLastFileOpen = None

        self.widgetTitle = QLabel("Session Setup")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        projectTextLabel = "Project"
        projectTextTemp = "Please type or select Project"
        listTextProject = [
            "",
            "Fowler Marshall - BMY Construction Group, Inc.",
            "SLO Hawthorne - HARRIS CONSTRUCTION CO INC",
            "Sanger Complex III - HARRIS CONSTRUCTION CO INC",
            "Sanger Aquatics - HARRIS CONSTRUCTION CO INC",
            "Parlier High - BMY Construction Group, Inc.",
            "Parlier Jr - BMY Construction Group, Inc.",
            "Avenal Tamarack - BMY Construction Group, Inc.",
        ]
        self.widgetComboxProject = Widgets.Combox(projectTextLabel, projectTextTemp, listTextProject, (90, 30))

        self.widgetInputCPR = Widgets.InputFieldLine("CPR ID", (240,30), (120, 30))
        self.widgetInputCPR.input.setPlaceholderText("FOR OPEN CPR ONLY")
        # self.widgetInputDateStart = Widgets.InputFieldLine("Week Start", (240,30), (120, 30))
        # self.widgetInputDateEnd = Widgets.InputFieldLine("Week End", (240,30), (120, 30))

        self.widgetExcelList = Widgets.ListDragDrop(self.pathExcelFolder, (240,240))
        self.widgetExcelBtnClear = Widgets.Button(self.widgetExcelList.clear_folder, "Clear Folder", (90,30))
        self.widgetExcelBtnOpen = Widgets.Button(self.widgetExcelList.open_folder, "Open Folder", (90,30))
        self.widgetExcelBtnAddFiles = Widgets.Button(self.widgetExcelList.add_files, "Add Files", (90,30))

        self.widgetJsonList = Widgets.ListDragDrop(self.pathJsonFolder, (240,240))
        self.widgetJsonBtnClear = Widgets.Button(self.widgetJsonList.clear_folder, "Clear Folder", (90,30))
        self.widgetJsonBtnOpen = Widgets.Button(self.widgetJsonList.open_folder, "Open Folder", (90,30))
        self.widgetJsonBtnAddFiles = Widgets.Button(self.widgetJsonList.add_files, "Add Files", (90,30))

        self.widgetLoad = Widgets.Button(self.load, "Load Session", (110, 30))

        self.setup_ui()

    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)
        layout.addWidget(self.widgetComboxProject)
        layout.addWidget(self.widgetInputCPR)
        # layout.addWidget(self.widgetInputDateStart)
        # layout.addWidget(self.widgetInputDateEnd)

        layoutFrame = QHBoxLayout()

        layoutFrameExcelList = QVBoxLayout()
        layoutFrameExcelList.addWidget(self.widgetExcelList)
        layoutFrameExcelListButtons = QHBoxLayout()
        layoutFrameExcelListButtons.addWidget(self.widgetExcelBtnClear, alignment=Qt.AlignLeft)
        layoutFrameExcelListButtons.addStretch()
        layoutFrameExcelListButtons.addWidget(self.widgetExcelBtnOpen)
        layoutFrameExcelListButtons.addWidget(self.widgetExcelBtnAddFiles, alignment=Qt.AlignRight)
        layoutFrameExcelList.addLayout(layoutFrameExcelListButtons)
        layoutFrame.addLayout(layoutFrameExcelList)

        layoutFrameJsonList = QVBoxLayout()
        layoutFrameJsonList.addWidget(self.widgetJsonList)
        layoutFrameJsonListButtons = QHBoxLayout()
        layoutFrameJsonListButtons.addWidget(self.widgetJsonBtnClear, alignment=Qt.AlignLeft)
        layoutFrameJsonListButtons.addStretch()
        layoutFrameJsonListButtons.addWidget(self.widgetJsonBtnOpen)
        layoutFrameJsonListButtons.addWidget(self.widgetJsonBtnAddFiles, alignment=Qt.AlignRight)
        layoutFrameJsonList.addLayout(layoutFrameJsonListButtons)
        layoutFrame.addLayout(layoutFrameJsonList)
        layout.addLayout(layoutFrame)

        layout.addWidget(self.widgetLoad, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)

    def get_project(self):
        return self.widgetComboxProject.combox.currentText().strip()
    
    def get_cpr(self):
        return self.widgetInputCPR.input.text().strip()


    def load(self):
        if self.get_project() == "": 
            return

        self.close_excel()
    
        if not os.path.exists(self.pathExcelFolder) or not os.path.exists(self.pathJsonFolder):
            return None
        
        excelList = sorted(os.listdir(self.pathExcelFolder))
        jsonList = sorted(os.listdir(self.pathJsonFolder))
        if len(excelList) == 0 or len(jsonList) == 0:
            return None
        
        fileNameExcel = excelList[0]
        fileNameJson = jsonList[0]
        pathExcelFile = os.path.join(self.pathExcelFolder, fileNameExcel)
        pathJsonFile = os.path.join(self.pathJsonFolder, fileNameJson)

        Widgets._clear_folder(self.pathInputFolder)
        Widgets._move_file_to_folder(pathExcelFile, self.pathInputFolder)
        Widgets._move_file_to_folder(pathJsonFile, self.pathInputFolder)

        pathFileToOpen = os.path.join(self.pathInputFolder, fileNameExcel)
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        pathExcelProgram = None
        for path in possible_paths:
            if os.path.exists(path):
                pathExcelProgram = path

        if not pathExcelProgram:
            print("No excel program found")
            return None
        
        try:
            subprocess.Popen([pathExcelProgram, "--view", pathFileToOpen])
            self.pathLastFileOpen = pathFileToOpen
        except Exception as e:
            print(f"Could not open Excel file: {e}")

        package = [self.get_project(), self.get_cpr()]
        self.signalProjectSelected.emit(package)
    
    def close_excel(self):
        if self.pathLastFileOpen is None:
            return

        try:
            from pywinauto.application import Application
            app = Application(backend="uia").connect(title_re=".*LibreOffice.*", timeout=5)
            app.top_window().close()
            print("Sent close signal to LibreOffice window")
        except Exception as e:
            print(f"Could not gracefully close LibreOffice: {e}")

        self.pathLastFileOpen = None





class PanelSession(QFrame):
    def __init__(self, _pathInputFolder: str, _pathOutputFolder: str, _pathMoveToRenamer: str, _pathLogFile: str):
        super().__init__()
        self.setObjectName("Panel")
        self.setStyleSheet(Style.FRAME_PANEL)

        self.pathExcelFile = None
        self.pathJsonFile = None
        self.sessionConfig = None
        self.sessionEntryData = None
        self.pathInputFolder = _pathInputFolder
        self.pathOutputFolder = _pathOutputFolder
        self.pathMoveToRenamer = _pathMoveToRenamer
        self.pathLogFile = _pathLogFile

        self.pathDownloadsFolder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.filesDownloadsContentOld = set(os.listdir(self.pathDownloadsFolder))

        self.watcherDownloads = QFileSystemWatcher()
        self.watcherDownloads.addPath(self.pathDownloadsFolder)
        self.watcherDownloads.directoryChanged.connect(self.on_file_added_to_downloads)

        self.widgetTitle = QLabel("Automation Sessions")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        self.widgetInputExcel = Widgets.SingleFileDrop()
        self.widgetInputJson = Widgets.SingleFileDrop()
        self.widgetEntryProject = Widgets.SingleFileDrop()
        self.widgetEntryPrime = Widgets.SingleFileDrop()

        self.widgetRun = Widgets.Button(self.run, "Run Entry")

        self.widgetOutputList = Widgets.ListDragDrop(self.pathOutputFolder, (240, 240))
        self.widgetOutputBtnClear = Widgets.Button(self.widgetOutputList.clear_folder, "Clear Folder", (90,30))
        self.widgetOutputBtnOpen = Widgets.Button(self.widgetOutputList.open_folder, "Open Folder", (90,30))

        self.widgetOutputBtnMoveRenamer = Widgets.Button(lambda: self.widgetOutputList.move_to_folder(self.pathMoveToRenamer), "Move To Renamer", (110,30))

        self.setup_ui()

    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)

        layoutSession = QHBoxLayout()

        layoutSessionInput = QVBoxLayout()
        layoutSessionInput.addWidget(self.widgetInputExcel)
        layoutSessionInput.addWidget(self.widgetInputJson)
        layoutSessionInput.addWidget(self.widgetEntryProject)
        layoutSessionInput.addWidget(self.widgetEntryPrime)
        layoutSession.addLayout(layoutSessionInput)

        layoutSessionButton = QVBoxLayout()
        layoutSessionButton.addStretch()
        layoutSessionButton.addWidget(self.widgetRun)
        layoutSessionButton.addStretch()
        layoutSession.addLayout(layoutSessionButton)
        layout.addLayout(layoutSession)
        
        layoutOutput = QVBoxLayout()
        layoutOutput.addWidget(self.widgetOutputList)

        layoutOutputButtons = QHBoxLayout()
        layoutOutputButtons.addWidget(self.widgetOutputBtnClear, alignment=Qt.AlignLeft)
        layoutOutputButtons.addStretch()
        layoutOutputButtons.addWidget(self.widgetOutputBtnOpen, alignment=Qt.AlignRight)
        layoutOutput.addLayout(layoutOutputButtons)
        layout.addLayout(layoutOutput)
        layout.addWidget(self.widgetOutputBtnMoveRenamer)
        self.setLayout(layout)


    def set_session_config(self, _package: list):
        projectSelcted = _package[0]
        if not isinstance(projectSelcted, str):
            return
        
        isCPR = _package[1]
        if not isinstance(isCPR, str):
            return
        
        self.sessionConfig = config.get(projectSelcted, None)
        if self.sessionConfig == None:
            return
        
        self.cprToOpen = None if isCPR == "" else isCPR

        if not os.path.exists(self.pathInputFolder):
            return None
        inputExcelList = [file for file in os.listdir(self.pathInputFolder) if file.endswith(".xlsx") or file.endswith(".xlsm")]
        inputJsonList = [file for file in os.listdir(self.pathInputFolder) if file.endswith(".json")]

        fileNameExcel = inputExcelList[0]
        fileNameJson = inputJsonList[0]
        self.pathExcelFile = os.path.join(self.pathInputFolder, fileNameExcel)
        self.pathJsonFile = os.path.join(self.pathInputFolder, fileNameJson)

        self.widgetInputExcel.set_file(self.pathExcelFile)
        self.widgetInputJson.set_file(self.pathJsonFile)
        self.widgetEntryProject.set_label(self.sessionConfig["project_name"])
        self.widgetEntryPrime.set_label(self.sessionConfig["prime_name"])

        with open(self.pathJsonFile, "r", encoding="utf-8") as file:
            self.sessionEntryData = json.load(file)
        
        self.configUser = config["username"]
        self.configPass = config["password"]
        self.configDIR = self.sessionConfig["project"]
        self.configPrime = self.sessionConfig["prime"]
        self.configPrimeName = self.sessionConfig["prime_name"]
        self.configIsOpen = False if self.cprToOpen == None else True
        self.configCPRId = self.cprToOpen
        self.configNonWork = False

    def on_file_added_to_downloads(self):
        filesDownloadsContentNew = set(os.listdir(self.pathDownloadsFolder))
        fileDiff = filesDownloadsContentNew - self.filesDownloadsContentOld

        for fileName in fileDiff:
            pathFile = os.path.join(self.pathDownloadsFolder, fileName)
            Widgets.safe_move_file(pathFile, self.pathOutputFolder)


    def run(self):
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

            Automate.s0_log_in(page, self.configUser, self.configPass, self.pathLogFile)
            Automate.s1_dismiss_announcement(page, self.pathLogFile)

            if self.configIsOpen:
                Automate.s1_project_dir_cpr_view(page, self.configDIR, self.pathLogFile)
                Automate.s2_cpr_index_id_open(page, self.configCPRId, self.pathLogFile)
            else:
                Automate.s1_project_dir_cpr_new(page, self.configDIR, self.pathLogFile)
    
            if self.configNonWork:
                Automate.s3_cpr_fill_non_work(page, self.configPrime, self.configPrimeName, self.sessionEntryData, self.pathLogFile)
            else:
                Automate.s3_cpr_fill(page, self.configPrime, self.configPrimeName, self.sessionEntryData, self.pathLogFile)

            context.close()
            browser.close()
    
        

class ScreenSession(QWidget):
    def __init__(self, _pathSession, _pathRenamer, _pathLogFile):
        super().__init__()
        self.pathSessionExcelFolder = _pathSession / "excel"
        self.pathSessionJsonFolder = _pathSession / "json"
        self.pathSessionInputFolder = _pathSession / "input"
        self.pathSessionOutputFolder = _pathSession / "output"
        self.pathRenamerInputFolder = _pathRenamer / "input"
        self.pathLogFile = _pathLogFile
    
        self.widgetPanelSetup = PanelSetup(self.pathSessionExcelFolder, self.pathSessionJsonFolder, self.pathSessionInputFolder, self.pathLogFile)
        self.widgetPanelSession = PanelSession(self.pathSessionInputFolder, self.pathSessionOutputFolder, self.pathRenamerInputFolder, self.pathLogFile)

        self.widgetPanelSetup.signalProjectSelected.connect(self.widgetPanelSession.set_session_config)

        self.setupUI()


    def setupUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetPanelSetup)
        layout.addWidget(self.widgetPanelSession)

        self.setLayout(layout)