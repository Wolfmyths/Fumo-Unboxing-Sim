from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer

from widgets.prizeQWidget import PrizeFrame
from widgets.gachaQGraphicsView import GachaRolls

from diceRoll import saveData

if TYPE_CHECKING:
    from src.diceRoll import Fumo
    from widgets.QMainWindow import MainWindow

class Gacha(qtw.QWidget):
    award: Fumo
    scrollingFrameOriginalPos: QPoint
    def __init__(self, parent: MainWindow):
        super().__init__(parent)
        self.qparent = parent

        # Window frame is box layout
        self.centralwidget = qtw.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.centeralWidgetLayout = qtw.QVBoxLayout()
        self.centeralWidgetLayout.setContentsMargins(15, 50, 15, 5)
        self.centeralWidgetLayout.setSpacing(10)

        # Frame
        self.borderFrame = qtw.QFrame(self.centralwidget)
        self.borderFrame.setObjectName('borderFrame')
        self.borderFrame.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
        borderframelayout = qtw.QVBoxLayout()
        self.borderFrame.setLayout(borderframelayout)
        self.centeralWidgetLayout.addWidget(self.borderFrame)

        # Frame
        self.bottomFrame = qtw.QFrame(self.centralwidget)
        self.bottomFrame.setObjectName('bottomFrame')
        self.bottomFrame.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
        self.centeralWidgetLayout.addWidget(self.bottomFrame)

        # Vertical Layout
        self.bottomFrameLayout = qtw.QHBoxLayout(self.bottomFrame)

        # Switch to Main Menu Button
        self.mainMenuButton = qtw.QPushButton('Main Menu', self.bottomFrame)
        self.mainMenuButton.clicked.connect(lambda: self.qparent.stackedWidget.setCurrentWidget(self.qparent.mainMenu))
        self.bottomFrameLayout.addWidget(self.mainMenuButton)

        # Button
        self.myButton = qtw.QPushButton(self.bottomFrame, text='Roll')
        self.myButton.clicked.connect(self.rollAnimation)
        self.bottomFrameLayout.addWidget(self.myButton)

        # FormGroupBox
        self.settingsGroupBox()

        # GraphicsView
        self.scrollingFrame = GachaRolls(self.borderFrame, self)
        borderframelayout.addWidget(self.scrollingFrame)
        self.scrollingFrameOriginalPos = self.scrollingFrame.pos()

        self.setLayout(self.centeralWidgetLayout)

    def rollAnimation(self):

        self.myButton.setEnabled(False)
        self.mainMenuButton.setEnabled(False)

        animationDuration = 5000 if not self.checkBox_fastroll.isChecked() else 3000
        #  Default duration ^                                   Faster Duration ^

        self.scrollingFrame.reRoll()

        prizeLocation = self.scrollingFrame.getPrizeLabelLocation().x() - 117

        # Scrolling Animation
        self.animation = QPropertyAnimation(self.scrollingFrame.horizontalScrollBar(), b'value')
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.setStartValue(0)
        self.animation.setEndValue(prizeLocation)
        self.animation.setDuration(animationDuration)
        self.animation.start()

        saveData().saveData(self.scrollingFrame.award.name)

        if not self.checkBox_awardWindow.isChecked():
            QTimer.singleShot(animationDuration, self.createAwardWindow)

        QTimer.singleShot(animationDuration, lambda: self.myButton.setEnabled(True))
        QTimer.singleShot(animationDuration, lambda: self.mainMenuButton.setEnabled(True))

    def createAwardWindow(self) -> None:
        self.awardWindow = PrizeFrame(self.scrollingFrame.award)
        self.awardWindow.show()

    def settingsGroupBox(self):
        self.formGroupBox = qtw.QGroupBox('Roll Settings', self)

        layout = qtw.QVBoxLayout(self.formGroupBox)

        # Fast Roll Checkbox
        self.checkBox_fastroll = qtw.QCheckBox('Fast Roll', self.formGroupBox)
        self.checkBox_fastroll.setChecked(False)
        layout.addWidget(self.checkBox_fastroll)

        # Skip Award Window Checkbox
        self.checkBox_awardWindow = qtw.QCheckBox('Skip Award Window', self.formGroupBox)
        self.checkBox_awardWindow.setChecked(False)
        layout.addWidget(self.checkBox_awardWindow)

        self.bottomFrameLayout.addWidget(self.formGroupBox)
