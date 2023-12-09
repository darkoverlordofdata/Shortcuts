import os
import sys
import configparser
from types import SimpleNamespace
from ShortcutModel import ShortcutModel
from QtSingleApplication import QtSingleApplication
from EditActionDialog import EditActionDialog

from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QProcess
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit, 
    QMainWindow, 
    QTableView, 
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QLabel, 
    QHeaderView,
    QPushButton
)



class MainWindow(QMainWindow):

    def addButton_onclick(self):
        self.data = SimpleNamespace(shortcut='', description='', enabled=False, command='')
        dlg = EditActionDialog(self.data)
        if dlg.exec():
            
            print('==========================')
            print(f'shortcut: {dlg.data.shortcut}')
            print(f'description: {dlg.data.description}')
            print(f'enabled: {dlg.data.enabled}')
            print(f'command: {dlg.data.command}')
            print('==========================')

        else:
            print('==========================')
            print('cancelled')
            print('==========================')

    def removeButton_onclick(self):
        pass

    def modifyButton_onclick(self):
        if self.id == -1:
            print('none selected')
        else:
            data = SimpleNamespace(
                shortcut=self.data[self.id][1], 
                description=self.data[self.id][2], 
                enabled=self.data[self.id][3], 
                command=self.data[self.id][4])

            dlg = EditActionDialog(data)
            if dlg.exec():
                print('==========================')
                print(f'shortcut: {dlg.data.shortcut}')
                print(f'description: {dlg.data.description}')
                print(f'enabled: {dlg.data.enabled}')
                print(f'command: {dlg.data.command}')
                print('==========================')

            else:
                print('==========================')
                print('cancelled')
                print('==========================')

    def closeButton_onclick(self):
        self.close()

    def table_onclick(self):
        index = self.table.selectedIndexes()[0]
        self.id = int(self.table.model().data(index))
        print("id    : " + str(self.id)) 
        print(self.data[self.id])


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shortcuts")
        self.setFixedWidth(750)
        self.setFixedHeight(400)

        font = QFont('Arial', 12, weight=QFont.Bold)
        
        config = configparser.RawConfigParser()
        config.read(f'{os.environ["HOME"]}/.config/kglobalshortcutsrc')

        sections = config.sections()
        self.data = []
        self.id = -1
        id = 0

        for type in sections:
            for info in config.options(type):
                row = config[type][info].split(",")
                if len(row) >= 3:
                    shortcut = row[0]
                    description = row[2]
                    self.data.append([id, shortcut, description, type, info])
                    id = id+1
                
        self.table = QTableView(minimumHeight=300)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        model = ShortcutModel(self.data, ["ID", "Shortcut", "Description", "Type", "Info"])
        self.table.setModel(model)
        self.table.clicked.connect(self.table_onclick)

        header = self.table.horizontalHeader()    
    
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setFont(font)

        addButton = QPushButton("Add")
        removeButton = QPushButton("Remove")
        modifyButton = QPushButton("Modify ...")
        closeButton = QPushButton("Close", maximumWidth=100)
        defaultButton = QPushButton("Default", maximumWidth=100)

        addButton.clicked.connect(self.addButton_onclick)
        removeButton.clicked.connect(self.removeButton_onclick)
        modifyButton.clicked.connect(self.modifyButton_onclick)
        closeButton.clicked.connect(self.closeButton_onclick)

        mainLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        topLeftLayout = QVBoxLayout()
        topRightLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()
        bottomLeftLayout = QVBoxLayout()
        bottomRightLayout = QVBoxLayout()

        searchFor = QLineEdit()
        searchFor.setPlaceholderText("Search")
        topLeftLayout.addWidget(searchFor)
        topLeftLayout.addWidget(self.table)

        topRightLayout.addWidget(addButton)
        topRightLayout.addWidget(removeButton)
        topRightLayout.addWidget(modifyButton)
        topRightLayout.addStretch()

        bottomLeftLayout.setAlignment(Qt.AlignLeft)
        bottomLeftLayout.addStretch()
        bottomLeftLayout.addWidget(defaultButton)

        bottomRightLayout.setAlignment(Qt.AlignRight)
        bottomRightLayout.addStretch()
        bottomRightLayout.addWidget(closeButton)

        topLayout.addLayout(topLeftLayout)
        topLayout.addLayout(topRightLayout)

        bottomLayout.addLayout(bottomLeftLayout)
        bottomLayout.addLayout(bottomRightLayout)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)


if __name__ == "__main__":
    
    app = QtSingleApplication('2991fed6-462e-47fe-b104-9dede758f1c8', sys.argv)
    if app.isRunning():
        sys.exit(0)
    w = MainWindow()
    w.show()
    app.setActivationWindow(w)
    sys.exit(app.exec_())