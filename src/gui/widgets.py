from PySide6.QtWidgets import (
    QListWidget, QPushButton, QWidget, QComboBox, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QFileSystemWatcher
from PySide6.QtGui import QDragMoveEvent, QDragEnterEvent, QDropEvent
import os
import shutil
import src.gui.style as Style


def _copy_files_to_folder(pathFile: str, pathFolder: str) -> bool:
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




class ListDragDrop(QListWidget):
    def __init__(self, pathFolder: str, minHeight: int, minWidth: int) -> None:
        super().__init__()

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setStyleSheet(Style.LIST_DRAG_DROP)
        self.setMinimumHeight(minHeight)
        self.setMinimumWidth(minWidth)
        
        self.pathFolder = str(pathFolder)
        os.makedirs(self.pathFolder, exist_ok=True)
        
        self.watcherFolder = QFileSystemWatcher()
        self.watcherFolder.addPath(self.pathFolder)
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
                _copy_files_to_folder(pathFile, self.pathFolder)

    def refresh_list(self):
        self.clear()
        if os.path.exists(self.pathFolder):
            for fileName in sorted(os.listdir(self.pathFolder)):
                fullPath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(fullPath):
                    self.addItem(fileName)



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



class ButtonPopFolder(Button):
    def __init__(self, _pathFolder: str, _label: str, _size: tuple=None) -> None:
        self.pathFolder = _pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)

        super().__init__(onClicked=lambda: _pop_from_folder(self.pathFolder), label=_label, size=_size)




class ButtonOpenFolder(Button):
    def __init__(self, _pathFolder: str, _label: str, _size: tuple=None) -> None:
        self.pathFolder = _pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)

        super().__init__(onClicked=self.open, label=_label, size=_size)

    def open(self):
        if os.path.exists(self.pathFolder):
            os.startfile(self.pathFolder)



class ButtonClearFolder(Button):
    def __init__(self, _pathFolder: str, _label: str, _size: tuple=None) -> None:
        self.pathFolder = _pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)

        super().__init__(onClicked=self.clear, label=_label, size=_size)

    def clear(self):
        if os.path.exists(self.pathFolder):
            for fileName in os.listdir(self.pathFolder):
                filePath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(filePath):
                    try:
                        os.remove(filePath)
                    except Exception as e:
                        print(f"Failed to delete {filePath}: {e}")




class ButtonAddFiles(Button):
    def __init__(self, _pathFolder: str, _label: str, _size: tuple=None) -> None:
        self.pathFolder = _pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)

        super().__init__(onClicked=self.add_files, label=_label, size=_size)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files To Add")
        if files:
            for pathFile in files:
                _copy_files_to_folder(pathFile, self.pathFolder)



class Combox(QWidget):
    def __init__(self, label: str, placeholder: str, data: list, sizeLabel: tuple=None, sizeCombox: tuple=None) -> None:
        super().__init__()

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



class InputFieldLine(QWidget):
    def __init__(self, label: str, sizeField: tuple=None, sizeLabel: tuple=None) -> None:
        super().__init__()

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
        


                
