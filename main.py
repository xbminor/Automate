import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedLayout

from src.gui.screenSetup import IndexFilesScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eCPR Automation - Setup Run")
        self.resize(900, 500)

        self.dirNumber = None
        self.primeId = None
        self.primeName = None

        self.stack = QStackedLayout()
        container = QWidget()
        container.setLayout(self.stack)
        self.setCentralWidget(container)

        self.loadStartScreen()

    def loadStartScreen(self):
        screen = IndexFilesScreen()
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
