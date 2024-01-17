import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from diceRoll import Fumo
from consts import ICON

class PrizeFrame(qtw.QWidget):
    def __init__(self, fumo: Fumo):
        super().__init__()
        
        self.fumo = fumo

        self.setObjectName('prizeFrame')
        self.setWindowTitle('Fumo Unboxing Simulator: Prize Window')
        self.setWindowIcon(qtg.QIcon(ICON))

        self.resize(400, 400)

        layout = qtw.QVBoxLayout()

        self.prizeAnnounce = qtw.QLabel(self)
        self.prizeAnnounce.setText(f'You found {self.fumo.name}!')

        prizePixmap = qtg.QPixmap(self.fumo.img)
        self.prizeLabel = qtw.QLabel(self)
        self.prizeLabel.setProperty('rarity', fumo.rarity)
        self.prizeLabel.setScaledContents(True)
        self.prizeLabel.setPixmap(prizePixmap)

        self.closeButton = qtw.QPushButton('Yippie!!!', self)
        self.closeButton.clicked.connect(self.deleteLater)

        for widget in (self.prizeAnnounce,
                       self.prizeLabel,
                       self.closeButton):
            layout.addWidget(widget)
        
        self.setLayout(layout)
