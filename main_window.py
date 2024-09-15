from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout,QMainWindow,QWidget,QMessageBox
from variables import BIG_FONT_SIZE,MINIMUM_WIDTH

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None= None,*args,**kwargs)  -> None:
        super().__init__(parent, *args, **kwargs)
        #configurando layout basico
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setWindowTitle('Calculadora')
        self.setCentralWidget(self.cw)


    def adjustfixedsize(self):
        #ultima coisa
        self.adjustSize()

    def addwidgetToVlayout(self,widget:QWidget):
        self.vLayout.addWidget(widget)
        self.adjustSize()

    def makeMsgBox(self):
        return QMessageBox(self)