from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt

from diceRoll import saveData
from consts import InventorySortValues

if TYPE_CHECKING:
    from widgets.QMainWindow import MainWindow

class Inventory(qtw.QWidget):
    def __init__(self, parent: MainWindow):
        super().__init__(parent)
        self.qparent = parent
        self.setObjectName('inventoryWindow')

        self.labelSettings = {'sort': InventorySortValues.rarity, 'ascending': False}

        self.qlayout = qtw.QVBoxLayout()

        # Frame
        self.inventoryFrame = qtw.QFrame(self)
        self.inventoryFrame.setObjectName('inventoryFrame')
        self.inventoryFrame.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
        self.qlayout.addWidget(self.inventoryFrame)

        # Scroll Area
        self.scrollAreaLayout = qtw.QHBoxLayout(self.inventoryFrame)
        self.scrollArea = qtw.QScrollArea(self.inventoryFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0,0,0,0)
        self.scrollAreaWidgetContents = qtw.QFrame()
        self.scrollAreaWidgetContents.setContentsMargins(0,0,0,0)
        self.gridLayout = qtw.QGridLayout(self.scrollAreaWidgetContents) # Grid Layout
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.addWidget(self.scrollArea)

        # Labels in Frames
        self.initLabels()

        # Frame
        self.bottomFrame = qtw.QFrame(self)
        self.bottomFrame.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
        self.qlayout.addWidget(self.bottomFrame)

        # Vertical Layout
        self.bottomFrameLayout = qtw.QVBoxLayout(self.bottomFrame)

        # Main Menu Button
        self.mainMenuButton = qtw.QPushButton('Main Menu', self.bottomFrame)
        self.mainMenuButton.clicked.connect(lambda: self.qparent.stackedWidget.setCurrentWidget(self.qparent.mainMenu))
        self.bottomFrameLayout.addWidget(self.mainMenuButton)

        # Reset Progress Button
        self.resetProgressButton = qtw.QPushButton('Reset Progress', self.bottomFrame)
        self.resetProgressButton.clicked.connect(self.deleteProgress)
        self.bottomFrameLayout.addWidget(self.resetProgressButton)

        # Button Group Box
        self.buttonGroupBox()

        self.setLayout(self.qlayout)

    def buttonGroupBox(self):
        # Group Box
        self.groupBox = qtw.QGroupBox()
        self.groupBox.setObjectName('buttonGroupBox')

        # Grid Layout
        layout = qtw.QGridLayout(self.groupBox)
        layout.setContentsMargins(2,2,2,2)

        # Button Group for Ascend/Descend buttons
        self.buttonGroupOrder = qtw.QButtonGroup(self.groupBox)
        self.buttonGroupOrder.setExclusive(True)

        # Ascend Button
        self.ascendButton = qtw.QPushButton('Ascending', self.groupBox, clicked = lambda: self.initLabels(ascending=True), checkable=True)
        self.ascendButton.setObjectName('groupBoxButton')
        self.buttonGroupOrder.addButton(self.ascendButton, 0)
        layout.addWidget(self.ascendButton, 2, 2, 2, 1)

        # Descend Button - Pressed on by default
        self.descendButton = qtw.QPushButton('Descending', self.groupBox, clicked = lambda: self.initLabels(ascending=False), checkable=True, checked=True)
        self.descendButton.setObjectName('groupBoxButton')
        self.buttonGroupOrder.addButton(self.descendButton, 1)
        layout.addWidget(self.descendButton, 0, 2, 2, 1)

        # Button Group for Sortmode Buttons
        self.buttonGroupSortmode = qtw.QButtonGroup(self.groupBox)
        self.buttonGroupSortmode.setExclusive(True)

        # Alphabetical Button
        self.ABCButton = qtw.QPushButton('Alphabetical', self.groupBox, clicked = lambda: self.initLabels(sort=InventorySortValues.abc), checkable=True)
        self.ABCButton.setObjectName('groupBoxButton')
        self.buttonGroupSortmode.addButton(self.ABCButton, 0)
        layout.addWidget(self.ABCButton, 0, 0, 2, 1)

        # Rarity Button - Pressed on by default
        self.rarityButton = qtw.QPushButton('Rarity', self.groupBox, clicked = lambda: self.initLabels(sort=InventorySortValues.rarity), checkable=True, checked=True)
        self.rarityButton.setObjectName('groupBoxButton')
        self.buttonGroupSortmode.addButton(self.rarityButton, 1)
        layout.addWidget(self.rarityButton, 2, 0, 2, 1)

        # Amount Button
        self.amountButton = qtw.QPushButton('Amount Collected', self.groupBox, clicked = lambda: self.initLabels(sort=InventorySortValues.amount), checkable=True)
        self.amountButton.setObjectName('groupBoxButton')
        self.buttonGroupSortmode.addButton(self.amountButton, 2)
        layout.addWidget(self.amountButton, 0, 1, 2, 1)

        # Recent Button
        self.recentButton = qtw.QPushButton('Recent', self.groupBox, clicked = lambda: self.initLabels(sort=InventorySortValues.recent), checkable=True)
        self.recentButton.setObjectName('groupBoxButton')
        self.buttonGroupSortmode.addButton(self.recentButton, 3)
        layout.addWidget(self.recentButton, 2, 1, 2, 1)

        
        self.bottomFrameLayout.addWidget(self.groupBox)

    def deleteProgress(self):

        dlg = qtw.QMessageBox(self)
        dlg.setWindowTitle('Fumo Unboxing Simulator - Confirmation')
        dlg.setText('Are you sure you want to delete your save data?')
        dlg.setStandardButtons(qtw.QMessageBox.StandardButton.Yes | qtw.QMessageBox.StandardButton.No)
        dlg.setIcon(qtw.QMessageBox.Icon.Warning)
        button = dlg.exec()

        if button == qtw.QMessageBox.StandardButton.Yes:
            saveData().deleteData()
            self.initLabels()
 
        
    def initLabels(self, **sortmode):

        characterList = saveData().charList()

        # Delete all labels to make room for the refreshed ones
        for fumo in characterList:
            frame: qtw.QFrame = self.findChild(qtw.QFrame, f'{fumo.name}-Frame')
            if frame is not None:
                frame.deleteLater()

        if sortmode:
            self.labelSettings.update(**sortmode)

        if self.labelSettings['sort'] is InventorySortValues.abc:

            characterList.sort(key=lambda x: x.name, reverse=True)

        elif self.labelSettings['sort'] is InventorySortValues.amount:

            characterList.sort(key=lambda x: x.getAmount(), reverse=True)

        elif self.labelSettings['sort'] is InventorySortValues.recent:

            for char in characterList:

                # If characters at -1 recent value stayed at -1 the list wouldn't sort properly
                if char.recent == -1:
                    char.recent = (len(characterList) + 1)
            
            characterList.sort(key=lambda x: x.recent, reverse=True)


        if not self.labelSettings['ascending']:
            characterList.reverse()

        col = 0
        row = 0

        for fumo in characterList:

            if col >= 5:
                col = 0
                row += 1

            # Layout
            qlayout = qtw.QVBoxLayout()

            # Frame
            self.labelFrame = qtw.QFrame()
            self.labelFrame.setObjectName(f'{fumo.name}-Frame')
            self.labelFrame.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)

            # Amount of image collected
            self.labelAmount = qtw.QLabel(self.labelFrame, text='0')
            self.labelAmount.setObjectName(f'{fumo.name}-labelAmount')
            self.labelAmount.setProperty('owned', 'false')
            self.labelAmount.setAlignment(Qt.AlignmentFlag.AlignLeft)

            qlayout.addWidget(self.labelAmount)

            # Image
            self.label = qtw.QLabel(self.labelFrame)
            self.label.setObjectName(f'{fumo.name}-Label')
            self.pixmap = qtg.QPixmap(fumo.sil)
            self.label.setScaledContents(True)
            self.label.setPixmap(self.pixmap)

            qlayout.addWidget(self.label)

            # Name Text
            self.labelNameText = qtw.QLabel(self.labelFrame, text='???')
            self.labelNameText.setAlignment(Qt.AlignmentFlag.AlignBottom)

            if fumo.getAmount() > 0:
                self.labelAmount.setText(str(fumo.amount))
                self.labelAmount.setProperty('owned', 'true')
                self.labelNameText.setText(str(fumo.name))
                self.label.setPixmap(qtg.QPixmap(fumo.img))

            qlayout.addWidget(self.labelNameText)

            self.labelFrame.setLayout(qlayout)

            self.gridLayout.addWidget(self.labelFrame, row, col)

            col += 1
