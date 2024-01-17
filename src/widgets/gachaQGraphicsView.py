from __future__ import annotations
from typing import TYPE_CHECKING

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt, QPointF

from diceRoll import generateCharacter

if TYPE_CHECKING:
    from widgets.gachaQWidget import Gacha

class GachaRolls(qtw.QGraphicsView):
    def __init__(self, parent: qtw.QFrame, gacha: Gacha):
        super().__init__(parent=parent)
        self.qparent = parent
        self.gacha = gacha

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.originalPos = self.pos()

        self.container = qtw.QGraphicsWidget()

        self.qscene = qtw.QGraphicsScene(self)
        self.qlayout = qtw.QGraphicsLinearLayout(Qt.Orientation.Horizontal)

        for i in range(40):

            label = qtw.QLabel()

            proxyWidget = qtw.QGraphicsProxyWidget()
            proxyWidget.setParent(self.container)
            proxyWidget.setObjectName(f'item{i}')
            proxyWidget.setWidget(label)

            self.qlayout.addItem(proxyWidget)

        self.reRoll()

        self.container.setLayout(self.qlayout)
        self.qscene.addItem(self.container)
        self.setScene(self.qscene)

    def getProxyWidget(self, index: int) -> qtw.QGraphicsProxyWidget:
        return self.container.findChild(qtw.QGraphicsProxyWidget, f'item{index}')

    def getPrizeLabelLocation(self) -> QPointF:
        proxyWidget = self.getProxyWidget(33)
        position = self.mapToScene(proxyWidget.pos().toPoint())
        position.setX(max(0, min(proxyWidget.x(), self.qscene.width() - self.width())))
        return position

    def reRoll(self):
        self.horizontalScrollBar().setValue(0)

        for i in range(40):
            fumo = generateCharacter()
            label: qtw.QLabel = self.getProxyWidget(i).widget()

            # Show the prize in the roll if award window is disabled
            newPixmap = qtg.QPixmap(fumo.sil) if i != 35 or not self.gacha.checkBox_awardWindow.isChecked() else qtg.QPixmap(fumo.img)
            label.setPixmap(newPixmap)
            label.setProperty('rarity', fumo.rarity)
            label.style().polish(label)

            if i == 35:
                self.award = fumo
    