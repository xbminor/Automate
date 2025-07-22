from PySide6.QtWidgets import (
    QWidget, QLabel,
    QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt, Signal, QObject
from playwright.sync_api import sync_playwright

import os, json
import src.gui.widgets as Widgets
import src.gui.style as Style
import src.automate as Automate

with open(r".\config.json", "r") as configFile: 
    config = json.load(configFile)



class PanelSetup(QWidget):
    signalProjectSelected = Signal(str)

    def __init__(self, pathFolderList: str, pathLog: str):
        super().__init__()

        self.widgetTitle = QLabel("Session Setup")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        projectTextLabel = "Project"
        projectTextTemp = "Please type or select Project"
        listTextProject = [
            "",
            "SLO Hawthorne - HARRIS CONSTRUCTION CO INC",
            "Sanger Complex III - HARRIS CONSTRUCTION CO INC",
            "Sanger Aquatics - HARRIS CONSTRUCTION CO INC",
            "Parlier High - BMY Construction Group, Inc.",
            "Parlier Jr - BMY Construction Group, Inc.",
            "Avenal Tamarack - BMY Construction Group, Inc.",
        ]
        self.widgetComboxProject = Widgets.Combox(projectTextLabel, projectTextTemp, listTextProject, (90, 30))

        self.pathFolderList = pathFolderList
        self.pathLog = pathLog
        self.widgetListFiles = Widgets.ListDragDrop(self.pathFolderList, 240, 240)

        self.widgetClear = Widgets.ButtonClearFolder(self.pathFolderList, "Clear Folder", (90, 30))
        self.widgetOpen = Widgets.ButtonOpenFolder(self.pathFolderList, "Open Folder", (90, 30))
        self.widgetAddFiles = Widgets.ButtonAddFiles(self.pathFolderList, "Add Files", (90, 30))
        

        self.widgetEntryName = QLabel("Entry: None")
        self.widgetEntryName.setStyleSheet(Style.LABEL_DEFAULT)
        self.widgetEntryProject = QLabel("Project: None")
        self.widgetEntryProject.setStyleSheet(Style.LABEL_DEFAULT)
        self.widgetEntryPrime = QLabel("Prime: None")
        self.widgetEntryPrime.setStyleSheet(Style.LABEL_DEFAULT)

        self.widgetLoad = Widgets.Button(self.load, "Load Session", (110, 30))
        

        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)
        layout.addWidget(self.widgetComboxProject)

        layoutList = QVBoxLayout()
        layoutList.addWidget(self.widgetListFiles)
        
        layoutListButtons = QHBoxLayout()
        layoutListButtons.addWidget(self.widgetClear, alignment=Qt.AlignLeft)
        layoutListButtons.addStretch()
        layoutListButtons.addWidget(self.widgetOpen)
        layoutListButtons.addWidget(self.widgetAddFiles, alignment=Qt.AlignRight)
        layoutList.addLayout(layoutListButtons)
        layout.addLayout(layoutList)


        layout.addWidget(self.widgetLoad, alignment=Qt.AlignmentFlag.AlignHCenter)
 
        self.setLayout(layout)

    def get_project(self):
        return self.widgetComboxProject.combox.currentText().strip()


    def load(self):
        if os.path.exists(self.pathFolderList):
            listFolder = sorted(os.listdir(self.pathFolderList))
            if len(listFolder) == 0:
                return None

        self.signalProjectSelected.emit(self.get_project())
        




class PanelSession(QWidget):
    def __init__(self, pathFolderList: str, pathLogFile: str):
        super().__init__()

        self.pathFolderList = pathFolderList
        self.pathLog = pathLogFile
        self.widgetTitle = QLabel("Automation Sessions")
        self.widgetTitle.setAlignment(Qt.AlignCenter)
        self.widgetTitle.setStyleSheet(Style.LABEL_TITLE)

        self.widgetEntryName = QLabel("Entry: None")
        self.widgetEntryName.setStyleSheet(Style.LABEL_DEFAULT)
        self.widgetEntryProject = QLabel("Project: None")
        self.widgetEntryProject.setStyleSheet(Style.LABEL_DEFAULT)
        self.widgetEntryPrime = QLabel("Prime: None")
        self.widgetEntryPrime.setStyleSheet(Style.LABEL_DEFAULT)

        self.widgetRun = Widgets.Button(self.run, "Run Entry")
        self.widgetNext = Widgets.Button(self.next, "Next Entry")

         
        self.widgetInputCPR = Widgets.InputFieldLine("CPR ID", (240,30), (120, 30))
        self.widgetInputCPR.input.setPlaceholderText("FOR OPEN CPR ONLY")
        self.widgetInputDateStart = Widgets.InputFieldLine("Week Start", (240,30), (120, 30))
        self.widgetInputDateEnd = Widgets.InputFieldLine("Week End", (240,30), (120, 30))

        self.sessionConfig = None
        self.sessionEntryData = None
        

        layout = QVBoxLayout()
        layout.addWidget(self.widgetTitle)

        layoutSession = QHBoxLayout()
        layoutSessionEntry = QVBoxLayout()
        layoutSessionEntry.addWidget(self.widgetEntryName)
        layoutSessionEntry.addWidget(self.widgetEntryProject)
        layoutSessionEntry.addWidget(self.widgetEntryPrime)
        layoutSession.addLayout(layoutSessionEntry)

        layoutSession.addStretch()

        layoutSessionOptions = QVBoxLayout()
        layoutSessionOptions.addWidget(self.widgetInputCPR)
        layoutSessionOptions.addWidget(self.widgetInputDateStart)
        layoutSessionOptions.addWidget(self.widgetInputDateEnd)
        layoutSession.addLayout(layoutSessionOptions)
        layout.addLayout(layoutSession)


        layoutControls = QHBoxLayout()
        layoutControls.addWidget(self.widgetRun)
        layoutControls.addWidget(self.widgetNext)
        layout.addLayout(layoutControls)



        self.setLayout(layout)

    def set_session_data(self):
        if os.path.exists(self.pathFolderList):
            listFolder = sorted(os.listdir(self.pathFolderList))
            if len(listFolder) == 0:
                return None

        fileName = listFolder[0]
        self.widgetEntryName.setText(f"Entry: {fileName}")

        pathFull = os.path.join(self.pathFolderList, fileName)
        with open(pathFull, "r", encoding="utf-8") as file:
            self.sessionEntryData = json.load(file)

        self.configUser = config["username"]
        self.configPass = config["password"]

    def set_session_config(self, _project: str):
        if not isinstance(_project, str):
            return
        
        self.sessionConfig = config.get(_project, None)
        print(self.sessionConfig)
        if self.sessionConfig == None:
            return
        
        self.widgetEntryProject.setText(f"Project: {self.sessionConfig["project_name"]}")
        self.widgetEntryPrime.setText(f"Prime: {self.sessionConfig["prime_name"]}")
            
        self.configDIR = self.sessionConfig["project"]
        self.configPrime = self.sessionConfig["prime"]
        self.configPrimeName = self.sessionConfig["prime_name"]
        self.set_session_data()



    def run(self):
        self.configCPRId = self.widgetInputCPR.input.text().strip()
        self.configIsOpen = False if self.configCPRId == "" else True
        self.configNonWork = (
            self.widgetInputDateStart.input.text().strip() != "" and 
            self.widgetInputDateStart.input.text().strip() != ""
        )

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

            Automate.s0_log_in(page, self.configUser, self.configPass, self.pathLog)
            Automate.s1_dismiss_announcement(page, self.pathLog)

            if self.configIsOpen:
                Automate.s1_project_dir_cpr_view(page, self.configDIR, self.pathLog)
                Automate.s2_cpr_index_id_open(page, self.configCPRId, self.pathLog)
            else:
                Automate.s1_project_dir_cpr_new(page, self.configDIR, self.pathLog)
    
            if self.configNonWork:
                Automate.s3_cpr_fill_non_work(page, self.configPrime, self.configPrimeName, self.sessionEntryData, self.pathLog)
            else:
                Automate.s3_cpr_fill(page, self.configPrime, self.configPrimeName, self.sessionEntryData, self.pathLog)

            context.close()
            browser.close()


    def next(self):
        self.widgetInputCPR.input.clear()
        self.widgetInputDateStart.input.clear()
        self.widgetInputDateEnd.input.clear()

        if self.configNonWork == False:
            if Widgets._pop_from_folder(self.pathFolderList):
                self.set_session_data()
    
        


class ScreenSession(QWidget):
    def __init__(self, _pathSession, _pathRenamer, _pathLogFile):
        super().__init__()
        self.pathSessionFolder = _pathSession
        self.pathRenamerFolder = _pathRenamer
        self.pathLogFile = _pathLogFile
    
        self.widgetPanelSetup = PanelSetup(self.pathSessionFolder, self.pathLogFile)
        self.widgetPanelSession = PanelSession(self.pathSessionFolder, self.pathLogFile)

        self.widgetPanelSetup.signalProjectSelected.connect(self.widgetPanelSession.set_session_config)

        self.setupUI()


    def setupUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.widgetPanelSetup)
        layout.addWidget(self.widgetPanelSession)

        self.setLayout(layout)