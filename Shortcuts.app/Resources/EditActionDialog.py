import os
import sys
import configparser
from types import SimpleNamespace
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
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Edit Action")
        self.setFixedWidth(400)
        self.setFixedHeight(286)
        self.data = {}

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.acceptAction)
        self.buttonBox.rejected.connect(self.rejectAction)

        self.layout = QVBoxLayout()

        formLayout = QFormLayout()
        self.shortcutLineEdit = QLineEdit(maximumWidth=80)
        self.shortcutLineEdit.setText(data.shortcut)
        self.descLineEdit = QLineEdit()
        self.descLineEdit.setText(data.description)
        self.enabledCheckBox = QCheckBox(text="Enabled")
        print(f'data.enabled = {data.enabled}')
        if data.shortcut == 'none':
            self.enabledCheckBox.setChecked(False)
        else:
            self.enabledCheckBox.setChecked(True)
        self.commandTextEdit = QPlainTextEdit()
        self.commandTextEdit.setPlainText(data.command)

        formLayout.addRow("Shortcut", self.shortcutLineEdit)
        formLayout.addRow("Description", self.descLineEdit)
        formLayout.addRow("",  self.enabledCheckBox)
        formLayout.addWidget( QHLine())
        formLayout.addRow("Command", self.commandTextEdit)

        self.layout.addLayout(formLayout)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


    def rejectAction(self):
        self.data = SimpleNamespace(shortcut='', description='', enabled=False, command='')
        self.reject()

    def acceptAction(self):
        self.data = SimpleNamespace(
            shortcut=self.shortcutLineEdit.text(), 
            description=self.descLineEdit.text(), 
            enabled=self.enabledCheckBox.isChecked(), 
            command=self.commandTextEdit.toPlainText())
        self.accept()
