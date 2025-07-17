from PySide6.QtWidgets import (
    QListWidget, QPushButton, QWidget, QComboBox, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QFileSystemWatcher
from PySide6.QtGui import QDragMoveEvent, QDragEnterEvent, QDropEvent
import os
import shutil



styleLabels = """ QLabel {
    font-size: 11pt;
    font-family: 'Segoe UI';
    font-weight: 700;
    }
"""

styleButtons = """ 
    QPushButton {
        font-size: 11pt;
        font-family: 'Segoe UI';
        font-weight: 400;
    }
"""

styleList = """ 
    QListWidget {
        border: 2px dashed #7F9DB9;
        border-radius: 8px;
        font-family: 'Segoe UI';
        font-weight: 200;
        font-size: 14px;
        color: #ffffff;
        padding: 9px;
    }

    QListWidget::item {
        background-color: #222222;
        border: 1px solid #555555;
    }

    QListWidget QScrollBar:vertical {
        background: #7F9DB9;
        width: 8px;
        margin: 0px;
    }

"""

styleList2 = """ 
    QListWidget {
        border-radius: 8px;
        font-family: 'Segoe UI';
        font-weight: 200;
        font-size: 14px;
        color: #ffffff;
        padding: 9px;
    }

    QListWidget::item {
        background-color: #222222;
        border: 1px solid #555555;
    }

    QListWidget QScrollBar:vertical {
        background: #7F9DB9;
        width: 8px;
        margin: 0px;
    }

"""



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



class Button(QPushButton):
    def __init__(self, onClicked, label: str=None, size: tuple=None) -> None:
        super().__init__()
        
        if label != None and isinstance(label, str):
            self.setText(label)

        if size != None and isinstance(label, tuple):
            self.setFixedSize(size[0], size[1])
    
        self.clicked.connect(onClicked)



class ListDragDrop(QListWidget):
    def __init__(self, pathFolder: str, minHeight: int, minWidth: int) -> None:
        super().__init__()

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setStyleSheet(styleList)
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



class ButtonFolderPop(QPushButton):
    def __init__(self, pathFolder: str, text: str, size: tuple=None) -> None:
        super().__init__()

        self.pathFolder = pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)
        
        self.setText(text)
        self.setFixedSize(size[0], size[1])
        self.clicked.connect(self.pop)


    def pop(self):
        if os.path.exists(self.pathFolder):
            listFolder = sorted(os.listdir(self.pathFolder))
            if len(listFolder) == 0:
                return None
            
            fileName = listFolder[0]
            pathfile = os.path.join(self.pathFolder, fileName)
            
            try:
                os.remove(pathfile)
                print(f"Removed: {fileName}")
            except Exception as e:
                print(f"Failed to remove {fileName}: {e}")




class ButtonFolderOpen(QPushButton):
    def __init__(self, pathFolder: str, text: str, size: tuple=None) -> None:
        super().__init__()

        self.pathFolder = pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)
        
        self.setText(text)
        self.setFixedSize(size[0], size[1])
        self.clicked.connect(self.open)


    def open(self):
        if os.path.exists(self.pathFolder):
            os.startfile(self.pathFolder)



class ButtonFolderClear(QPushButton):
    def __init__(self, pathFolder: str, text: str, size: tuple=None) -> None:
        super().__init__()

        self.pathFolder = pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)
        
        self.setText(text)
        self.setFixedSize(size[0], size[1])
        self.clicked.connect(self.clear)


    def clear(self):
        if os.path.exists(self.pathFolder):
            for fileName in os.listdir(self.pathFolder):
                filePath = os.path.join(self.pathFolder, fileName)
                if os.path.isfile(filePath):
                    try:
                        os.remove(filePath)
                    except Exception as e:
                        print(f"Failed to delete {filePath}: {e}")






class ButtonFolderAddFiles(QPushButton):
    def __init__(self, pathFolder: str, text: str, size: tuple=None) -> None:
        super().__init__()

        self.pathFolder = pathFolder
        os.makedirs(self.pathFolder, exist_ok=True)
        
        self.setText(text)
        self.setFixedSize(size[0], size[1])
        self.clicked.connect(self.add_files)


    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files To Add")
        if files:
            for pathFile in files:
                _copy_files_to_folder(pathFile, self.pathFolder)



class Combox(QWidget):
    def __init__(self, label: str, placeholder: str, data: list, sizeLabel: tuple=None, sizeCombox: tuple=None) -> None:
        super().__init__()

        self.label = QLabel(label)
        self.label.setStyleSheet(styleLabels)
        if sizeLabel != None:
            self.label.setFixedSize(sizeLabel[0], sizeLabel[1])

        self.combox = QComboBox()
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
        self.input.setText(str(1))
        if sizeField != None:
            self.input.setFixedSize(sizeField[0], sizeField[1])

        self.label = QLabel(label)
        self.label.setStyleSheet(styleLabels)
        if sizeLabel != None:
            self.label.setFixedSize(sizeLabel[0], sizeLabel[1])

        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        self.setLayout(layout)
        


                
