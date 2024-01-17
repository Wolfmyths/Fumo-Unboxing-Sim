from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.QMainWindow import MainWindow

class MainMenu(qtw.QWidget):
    def __init__(self, parent: MainWindow) -> None:
        super().__init__(parent)
        self.qparent = parent

        self.qlayout = qtw.QVBoxLayout()
        self.qlayout.setContentsMargins(200, 400, 200, 400)

        # Label
        self.title = qtw.QLabel(self, text='Fumo\nUnboxing\nSimulator')
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Button to play gacha
        self.gachaButton = qtw.QPushButton('Gacha', self)
        self.gachaButton.clicked.connect(lambda: self.qparent.stackedWidget.setCurrentWidget(self.qparent.gacha))

        # Button to see inventory
        self.inventoryButton = qtw.QPushButton('Inventory', self)
        self.inventoryButton.clicked.connect(lambda: self.qparent.stackedWidget.setCurrentWidget(self.qparent.inventory))

        for widget in (self.title,
                       self.gachaButton,
                       self.inventoryButton):
            self.qlayout.addWidget(widget)

        self.setLayout(self.qlayout)
