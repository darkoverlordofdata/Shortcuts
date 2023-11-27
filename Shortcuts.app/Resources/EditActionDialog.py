import os
import sys
import configparser
from ShortcutModel import ShortcutModel
from QtSingleApplication import QtSingleApplication

from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QProcess
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QLineEdit, 
    QMainWindow, 
    QPlainTextEdit,
    QTableView, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QLabel, 
    QHeaderView,
    QPushButton
)

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class EditActionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit Action")
        self.setFixedWidth(400)
        self.setFixedHeight(286)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        formLayout = QFormLayout()
        shortcutLineEdit = QLineEdit(maximumWidth=80)
        descLineEdit = QLineEdit()
        enabledCheckBox = QCheckBox(text="Enabled")
        commandTextEdit = QPlainTextEdit()

        formLayout.addRow("Shortcut", shortcutLineEdit)
        formLayout.addRow("Description", descLineEdit)
        formLayout.addRow("",  enabledCheckBox)
        formLayout.addWidget( QHLine())
        formLayout.addRow("Command", commandTextEdit)

        self.layout.addLayout(formLayout)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
