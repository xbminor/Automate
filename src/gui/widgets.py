from PySide6.QtWidgets import (
    QListWidget, QPushButton, QComboBox, QLabel, QFrame, QWidget, QListWidgetItem,
    QFileDialog, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QFileSystemWatcher
from PySide6.QtGui import QDragMoveEvent, QDragEnterEvent, QDropEvent
import os
import shutil
import src.gui.style as Style

from PySide6.QtCore import QSize


def _copy_file_to_folder(pathFile: str, pathFolder: str) -> bool:
    try:
        if not os.path.isfile(pathFile):
            raise FileNotFoundError(f"{pathFile} is not valid file.")
    
        fileName = os.path.basename(pathFile)
        pathOutput = os.path.join(pathFolder, fileName)

        shutil.copy2(pathFile, pathOutput)
        return True
    except Exception as e:
        print(f"Failed to copy {pathFile} → {pathFolder}: {e}")
        return False


def _pop_from_folder(pathFolder: str):
    if os.path.exists(pathFolder):
        listFolder = sorted(os.listdir(pathFolder))
        if len(listFolder) == 0:
            return False
            
    fileName = listFolder[0]
    pathfile = os.path.join(pathFolder, fileName)
            
    try:
        os.remove(pathfile)
        print(f"Removed: {fileName}")
        return True
    except Exception as e:
        print(f"Failed to remove {fileName}: {e}")        
        return False

def _move_file_to_folder(_pathFile: str, _pathMoveToFolder: str):
    try:
        if not os.path.exists(_pathMoveToFolder):
            raise NotADirectoryError(f"{_pathMoveToFolder} is not valid folder.")
    
        if not os.path.isfile(_pathFile):
            raise FileNotFoundError(f"{_pathFile} is not valid file.")
    
        fileName = os.path.basename(_pathFile)
        pathDst = os.path.join(_pathMoveToFolder, fileName)

        shutil.move(_pathFile, pathDst)
        return True
    except Exception as e:
        print(f"Failed to move {fileName}: {e}")
        return False
    
def _clear_folder(pathFolder):
    if os.path.exists(pathFolder):
        for fileName in os.listdir(pathFolder):
            filePath = os.path.join(pathFolder, fileName)
            if os.path.isfile(filePath):
                try:
                    os.remove(filePath)
                except Exception as e:
                    print(f"Failed to delete {filePath}: {e}")
                



class ListDragDrop(QListWidget):
    def __init__(self, _pathFolder: str, _size: tuple=(240,240)) -> None:
        super().__init__()

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setStyleSheet(Style.LIST_DRAG_DROP)
        self.setMinimumSize(*_size)
        
        self.pathFolder = _pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)
        
        self.watcherFolder = QFileSystemWatcher()
        self.watcherFolder.addPath(str(self.pathFolder))
        self.watcherFolder.directoryChanged.connect(self.refresh_list)
        self.refresh_list()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                pathFile = url.toLocalFile()
                _copy_file_to_folder(pathFile, self.pathFolder)

    def refresh_list(self):
        self.clear()
        if os.path.exists(self.pathFolder):
            for fileName in sorted(os.listdir(self.pathFolder)):
                fullPath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(fullPath):
                    self.addItem(fileName)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files To Add")
        if files:
            for pathFile in files:
                _copy_file_to_folder(pathFile, self.pathFolder)

    def open_folder(self):
        if os.path.exists(self.pathFolder):
            os.startfile(self.pathFolder)

    def clear_folder(self):
        if os.path.exists(self.pathFolder):
            for fileName in os.listdir(self.pathFolder):
                filePath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(filePath):
                    try:
                        os.remove(filePath)
                    except Exception as e:
                        print(f"Failed to delete {filePath}: {e}")

    def move_to_folder(self, _pathMoveToFolder: str):
        if not os.path.exists(_pathMoveToFolder):
            return None
        
        for fileName in os.listdir(self.pathFolder):
            pathSrc = os.path.join(self.pathFolder, fileName)
            pathDst = os.path.join(_pathMoveToFolder, fileName)
            if os.path.isfile(pathSrc):
                try:
                    shutil.move(pathSrc, pathDst)
                except Exception as e:
                    print(f"Failed to move {fileName}: {e}")



class Button(QPushButton):
    def __init__(self, onClicked=None, label: str=None, size: tuple=None) -> None:
        super().__init__()
        self.setStyleSheet(Style.BUTTON_DEFAULT)
        
        if label != None and isinstance(label, str):
            self.setText(label)

        if size != None and isinstance(label, tuple):
            self.setFixedSize(size[0], size[1])
    
        if onClicked:
            self.clicked.connect(onClicked)




class SingleFileDrop(QWidget):
    def __init__(self, _size: tuple=(240, 50)) -> None:
        super().__init__()

        self.setAcceptDrops(True)
        self.setFixedSize(*_size)
        self.pathFile = None

        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, _size[0], _size[1])
        self.label.setStyleSheet("""
            QLabel {
                font-family: Segoe UI;
                font-size: 12pt;
                font-weight: 550;
                border: 2px dashed #3D6480;
                border-radius: 6px;
                background-color: #ABABAB;
                color: #000000;
            }
        """)

    def add_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Files To Add")
        if file:
            print(file)
            # _copy_file_to_folder(pathFile, self.pathFolder)
                

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.set_file(urls[0].toLocalFile())

    def set_file(self, filePath: str):
        if os.path.isfile(filePath):
            self.pathFile = filePath
            self.refresh()

    def set_label(self, label: str=None):
        if not label:
            return None
        
        self.label.setText(label)


    def refresh(self):
        if self.pathFile:
            fileName = os.path.basename(self.pathFile)
            self.label.setText(fileName)

    def clear_file(self):
        self.pathFile = None
        self.label.setText("")

    def get_file(self):
        return self.pathFile



class Combox(QFrame):
    def __init__(self, label: str, placeholder: str, data: list, sizeLabel: tuple=None, sizeCombox: tuple=None) -> None:
        super().__init__()

        self.setObjectName("Combox")
        self.setStyleSheet(Style.FRAME_COMBOX)

        self.label = QLabel(label)
        self.label.setStyleSheet(Style.LABEL_HEADING)
        if sizeLabel != None:
            self.label.setFixedSize(sizeLabel[0], sizeLabel[1])

        self.combox = QComboBox()
        self.combox.setStyleSheet(Style.COMBOX_DEFAULT)
        self.combox.setEditable(True)
        self.combox.addItems(data)
        self.combox.lineEdit().setPlaceholderText(placeholder)
        self.combox.setInsertPolicy(QComboBox.NoInsert)
        self.combox.setCompleter(self.combox.completer())
        if sizeCombox != None:
            self.combox.setFixedSize(sizeCombox[0], sizeCombox[1])

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combox)

        self.setLayout(layout)



class InputFieldLine(QFrame):
    def __init__(self, label: str, sizeField: tuple=None, sizeLabel: tuple=None) -> None:
        super().__init__()
        self.setObjectName("InputField")
        self.setStyleSheet(Style.FRAME_INPUT)

        self.input = QLineEdit()
        self.input.setStyleSheet(Style.INPUT_DEFAULT)
        if sizeField != None:
            self.input.setFixedSize(sizeField[0], sizeField[1])

        self.label = QLabel(label)
        self.label.setStyleSheet(Style.LABEL_HEADING)
        if sizeLabel != None:
            self.label.setFixedSize(sizeLabel[0], sizeLabel[1])

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        self.setLayout(layout)