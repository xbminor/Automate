from PySide6.QtWidgets import (
    QWidget, QLabel, QComboBox, QVBoxLayout, QPushButton
)
from PySide6.QtCore import Qt

class StartScreen(QWidget):
    def __init__(self, onContinueCallback):
        super().__init__()
        self.onContinueCallback = onContinueCallback
        self.setWindowTitle("DIR eCPR Automation")
        self.setupUi()
    
    def setupUi(self):
        layout = QVBoxLayout()

        # DIR Project Number
        labelDIR = QLabel("Project DIR:")
        self.comboxDIR = QComboBox()
        self.comboxDIR.setEditable(True)
        listDataDIR = [
            "",
            "506809 - Sanger Complex III - HARRIS CONSTRUCTION CO INC",
            "506782 - Sanger Aquatics - HARRIS CONSTRUCTION CO INC",
            "496589 - Parlier High - BMY Construction Group, Inc.",
            "493551 - Avenal Tamarack - BMY Construction Group, Inc."
        ]
        self.comboxDIR.addItems(listDataDIR)
        self.comboxDIR.lineEdit().setPlaceholderText("Select or type project DIR")
        self.comboxDIR.setInsertPolicy(QComboBox.NoInsert)
        self.comboxDIR.setCompleter(self.comboxDIR.completer())
        

        # Continue Button
        self.btnContinue = QPushButton("Continue")
        self.btnContinue.setEnabled(False)
        self.btnContinue.clicked.connect(self.onContinue)

        # Reactivity
        self.comboxDIR.lineEdit().textChanged.connect(self.validateInputs)

        # Layout assembly
        layout.addWidget(labelDIR)
        layout.addWidget(self.comboxDIR)
        layout.addWidget(self.btnContinue, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def validateInputs(self):
        isDirFilled = self.comboxDIR.currentText().strip() != ""
        self.btnContinue.setEnabled(isDirFilled)

    def onContinue(self):
        dirNumber = self.comboxDIR.currentText().strip()

        self.onContinueCallback(dirNumber)
