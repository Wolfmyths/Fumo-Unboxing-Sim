import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from widgets.QMainWindow import MainWindow

from consts import ICON, STYLESHEET

if __name__ == '__main__':
    import sys

    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon(ICON))

    with open(STYLESHEET, 'r') as f:
        app.setStyleSheet(f.read())

    mw = MainWindow()
    mw.show()

    app.exec()
