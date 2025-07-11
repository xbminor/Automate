import os
import re
import sys
import shutil
from src.renamer import gui_bulk_file_index_by_date
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QLabel, QListWidget, QPushButton, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit  
)
from PySide6.QtCore import Qt, QFileSystemWatcher
from PySide6.QtGui import QDragEnterEvent, QDropEvent



styleText = """ QLabel {
    font-size: 11pt;
    font-family: 'Segoe UI';
    font-weight: 1000;
    }
"""

def play_beep():
    if sys.platform.startswith("win"):
        import winsound
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    else:
        print("\a")  # POSIX fallback: terminal bell (may be silent)

class WidgetList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(False)  # explicitly disable dropping here
        self.setStyleSheet("border: 1px solid #666; padding: 10px;")  # look like display, not a drop zone
        self.setMinimumHeight(240)  # doubled height

class WidgetDrop(QLabel):
    def __init__(self, onFilesDropped, widgetList: QListWidget):
        super().__init__("Drop files")
        self.setFixedHeight(40)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                font-size: 12px;
                color: #666;
            }
        """)
        self.setAcceptDrops(True)
        self.listDisplay = widgetList
        self.onFilesDropped = onFilesDropped

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            if url.isLocalFile():
                files.append(url.toLocalFile())
        self.listDisplay.addItems(files)
        self.onFilesDropped(files)


class PanelCombox(QWidget):
    def __init__(self, title: str, placeholder: str, data: list):
        super().__init__()
        self.setLayout(QHBoxLayout())

        self.label = QLabel(title)
        self.label.setStyleSheet(styleText)
        self.label.setFixedWidth(90)

        self.combox = QComboBox()
        self.combox.setEditable(True)
        self.combox.addItems(data)
        self.combox.lineEdit().setPlaceholderText(placeholder)
        self.combox.setInsertPolicy(QComboBox.NoInsert)
        self.combox.setCompleter(self.combox.completer())

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.combox)
    


class PanelIndex(QWidget):
    def __init__(self, title: str, pathFolder: str, isEnabled: bool):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.label = QLabel(title)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.pathFolder = pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)
        self.listFiles = WidgetList()
        self.folderWatcher = QFileSystemWatcher()
        self.folderWatcher.addPath(self.pathFolder)
        self.folderWatcher.directoryChanged.connect(self.refresh_list)
        self.refresh_list()

        self.dropZone = WidgetDrop(self.handle_files_added, self.listFiles)

        self.btnClear = QPushButton("Clear")
        self.btnBrowse = QPushButton("Browse")
        self.btnClear.setFixedWidth(70)
        self.btnClear.clicked.connect(self.clear_files)
        self.btnBrowse.setFixedWidth(70)
        self.btnBrowse.clicked.connect(self.browse_files)

        self.isEnabledPanel = isEnabled
        self.set_enabled_state(isEnabled)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.btnClear, alignment=Qt.AlignLeft)
        btnLayout.addStretch()
        btnLayout.addWidget(self.btnBrowse, alignment=Qt.AlignRight)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.listFiles)
        self.layout().addWidget(self.dropZone)
        self.layout().addLayout(btnLayout)


    def set_enabled_state(self, isEnabled: bool):
        self.isEnabledPanel = isEnabled

        self.dropZone.setAcceptDrops(isEnabled)
        self.btnBrowse.setEnabled(isEnabled)




    def refresh_list(self):
        self.listFiles.clear()
        if os.path.exists(self.pathFolder):
            for fileName in sorted(os.listdir(self.pathFolder)):
                fullPath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(fullPath):
                    self.listFiles.addItem(fileName)


    def handle_files_added(self, files):
        for filePath in files:
            if not os.path.isfile(filePath):
                continue
            fileName = os.path.basename(filePath)
            destPath = os.path.join(self.pathFolder, fileName)

            try:
                shutil.copy2(filePath, destPath)
            except Exception as e:
                print(f"Failed to copy {filePath} → {destPath}: {e}")
        self.refresh_list()

    def browse_files(self):
        if not self.isEnabledPanel:
            play_beep()
            return
        
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.handle_files_added(files)
    
    def clear_files(self):
        if os.path.exists(self.pathFolder):
            for fileName in os.listdir(self.pathFolder):
                filePath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(filePath):
                    try:
                        os.remove(filePath)
                    except Exception as e:
                        print(f"Failed to delete {filePath}: {e}")
        self.refresh_list()






class IndexFilesScreen(QWidget):
    def __init__(self):
        super().__init__()
        pathRoot = Path(__file__).resolve().parents[2]
        pathToIndex = pathRoot / "data" / "to_index"
        pathWithIndex = pathRoot / "data" / "with_index"
        self.pathToIndex = str(pathToIndex)
        self.pathWithIndex = str(pathWithIndex)
        os.makedirs(self.pathToIndex, exist_ok=True)
        os.makedirs(self.pathWithIndex, exist_ok=True)
        self.setupUi()

    def setupUi(self):

        # DIR Project Number
        labelDIR = "Project DIR:"
        listDIR = [
            "",
            "506809 - Sanger Complex III - HARRIS CONSTRUCTION CO INC",
            "506782 - Sanger Aquatics - HARRIS CONSTRUCTION CO INC",
            "496589 - Parlier High - BMY Construction Group, Inc.",
            "493551 - Avenal Tamarack - BMY Construction Group, Inc."
        ]
        textDir = "Please type or select Project DIR or Name"
        self.comboxDIR = PanelCombox(labelDIR, textDir, listDIR)

        labelPrime = "Prime:"
        listPrime = [
            "",
            "113061 - HARRIS CONSTRUCTION CO INC",
            "686178 - BMY Construction Group, Inc.",
        ]
        textPrime = "Please type or select Prime ID or Name"
        self.comboxPrime = PanelCombox(labelPrime, textPrime, listPrime)

        self.labelTitle = QLabel("File Indexer")
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setStyleSheet(styleText)
        
        self.checkTitle = QLabel("Reverse Mode")
        self.check = QCheckBox()
        self.check.setChecked(False)
        self.check.stateChanged.connect(self.check_toggle)
        
        self.indexStart = 1
        self.inputStartIndex = QLineEdit()
        self.inputStartIndex.setFixedWidth(50)
        self.inputStartIndex.setText(str(self.indexStart))
        self.indexStartTitle = QLabel("Starting Index")
        
        self.panelInput = PanelIndex("Files to Index", self.pathToIndex, not self.check.isChecked())
        self.panelOutput = PanelIndex("Expected Output", self.pathWithIndex, self.check.isChecked())
        
        
        self.btnRun = QPushButton("RUN")
        self.btnRun.setFixedWidth(100)
        self.btnRun.clicked.connect(self.run_renamer)
        self.arrow = QLabel("→")

        self.labelRunStatus = QLabel("Default Mode")
       

        layout = QVBoxLayout()
        layout.addWidget(self.comboxDIR)
        layout.addWidget(self.comboxPrime)
        layout.addWidget(self.labelTitle)
        
        layoutIndexConfig = QHBoxLayout()
        layoutIndexConfig.addWidget(self.inputStartIndex)
        layoutIndexConfig.addWidget(self.indexStartTitle)
        layoutIndexConfig.addStretch()
        layoutIndexConfig.addWidget(self.checkTitle)
        layoutIndexConfig.addWidget(self.check)
        layout.addLayout(layoutIndexConfig)

        layoutIndex = QHBoxLayout()
        layoutIndex.addWidget(self.panelInput)

        layoutIndexCenter = QVBoxLayout()
        layoutIndexCenter.addStretch()
        layoutIndexCenter.addWidget(self.labelRunStatus, alignment=Qt.AlignCenter)
        layoutIndexCenter.addWidget(self.arrow, alignment=Qt.AlignCenter)
        layoutIndexCenter.addWidget(self.btnRun, alignment=Qt.AlignCenter)
        layoutIndexCenter.addStretch()
        layoutIndex.addLayout(layoutIndexCenter)
        layoutIndex.addWidget(self.panelOutput)
        layout.addLayout(layoutIndex)


        self.setLayout(layout)




    def check_toggle(self, state):
        if state == 2:
            self.panelInput.set_enabled_state(False)
            self.panelOutput.set_enabled_state(True)
            self.labelRunStatus.setText("Reverse Mode")
            self.arrow.setText("←")
        else:
            self.panelInput.set_enabled_state(True)
            self.panelOutput.set_enabled_state(False)
            self.labelRunStatus.setText("Default Mode")
            self.arrow.setText("→")


    def run_renamer(self):
        if not self.check.isChecked():
            # Forward Mode → add index by date
            gui_bulk_file_index_by_date(self.pathToIndex, self.pathWithIndex, self.indexStart)
            self.panelInput.refresh_list()
        else:
            # Reverse Mode → remove index
            prefixPattern = re.compile(r"^\d+_")

            renamedAny = False
            for fileName in os.listdir(self.pathWithIndex):
                fullPath = os.path.join(self.pathWithIndex, fileName)
                if os.path.isfile(fullPath) and prefixPattern.match(fileName):
                    newName = prefixPattern.sub("", fileName)
                    os.rename(fullPath, os.path.join(self.pathToIndex, newName))
                    renamedAny = True

            if renamedAny:
                print("Removed index prefixes.")
            else:
                print("No indexed files found to rename.")



