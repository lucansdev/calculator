import sys
from PySide6.QtWidgets import QApplication,QLabel,QLineEdit
from main_window import MainWindow
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH
from display import Display
from info import Info
from styles import setupTheme
from buttons import Button
from buttons import ButtonsGrid

if __name__ == "__main__":
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()


    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #info
    info = Info()
    window.addwidgetToVlayout(info)


    #display
    display = Display()
    window.addwidgetToVlayout(display)

    #grid
    buttonsGrid = ButtonsGrid(display,info,window)
    window.vLayout.addLayout(buttonsGrid)


    window.adjustfixedsize()

    window.show()
    app.exec()