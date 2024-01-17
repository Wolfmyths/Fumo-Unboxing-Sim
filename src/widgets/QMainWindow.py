import PySide6.QtWidgets as qtw

from widgets.gachaQWidget import Gacha
from widgets.inventoryQWidget import Inventory
from widgets.mainMenuQWidget import MainMenu

from consts import WindowTitles, VERSION

class MainWindow(qtw.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.resize(1920, 1080)

        self.mainMenu = MainMenu(self)
        self.inventory = Inventory(self)
        self.gacha = Gacha(self)

        self.qlayout = qtw.QVBoxLayout()

        self.stackedWidget = qtw.QStackedWidget()
        self.stackedWidget.currentChanged.connect(lambda: self.changeWindowTitle(self.stackedWidget.currentWidget()))

        for widget in (self.mainMenu,
                       self.inventory,
                       self.gacha):

            self.stackedWidget.addWidget(widget)

        self.stackedWidget.setCurrentWidget(self.mainMenu)

        self.qlayout.addWidget(self.stackedWidget)
        self.setCentralWidget(self.stackedWidget)
        self.setLayout(self.qlayout)

    def changeWindowTitle(self, widget: Gacha | Inventory | MainMenu) -> None:

        title: WindowTitles
        if isinstance(widget, Gacha):
            title = WindowTitles.getTitle(WindowTitles.gacha)

        elif isinstance(widget, Inventory):
            title = WindowTitles.getTitle(WindowTitles.inventory)

        elif isinstance(widget, MainMenu):
            title = WindowTitles.getTitle(WindowTitles.main_menu)

        self.setWindowTitle(f'Fumo Gacha Simulator V{VERSION}: {title}')
