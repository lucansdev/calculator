from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton,QGridLayout
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber,convertToNumber
from display import Display
from PySide6.QtCore import Slot
import math

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow

class Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75,75)


class ButtonsGrid(QGridLayout):
    def __init__(self,display:"Display",info:"Info",window:"MainWindow",*args,**kwargs):
        super().__init__(*args,**kwargs)

        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]

        self.display = display
        self.info = info
        self.window = window
        self._equation = "qualquer coisa"
        self._equationInitialValue = "sua conta"
        self._left = None
        self._right = None
        self._op = None
        self.equation =  self._equationInitialValue
        self._makeGrid()


    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self,value):
        self._equation = value
        self.info.setText(value)

    def vouApagarVoce(self):
        print("vou apagar voce",type(self))

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.clearPressed.connect(self._clear)
        self.display.delPressed.connect(self._backSpace)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                Slot = self._makeSlot(self._insertToDisplay,buttonText)
                self.addWidget(button, rowNumber, colNumber)
                self._connectButtonClicked(button,Slot)

    def _connectButtonClicked(self,button,slot):
        button.clicked.connect(slot)
    
    def _configSpecialButton(self,button):
        texto = button.text()
        if texto == "C":
            #slot = self._makeSlot(self.display.clear)
            self._connectButtonClicked(button,self._clear)
            #button.clicked.connect(self.display.clear)
        
        if texto in "+-/*^":
            self._connectButtonClicked(button,self._makeSlot(self._configLeftOp,texto))

        if texto == "=":
            self._connectButtonClicked(button,self._eq)

        if texto == "D":
            self._connectButtonClicked(button,self.display.backspace)
        
        if texto == "N":
            self._connectButtonClicked(button,self._invertNumber)

        

    def _makeSlot(self,func,*args,**kwargs):
        @Slot(bool)
        def realSlot():
            func(*args,**kwargs)
        return realSlot
    
    @Slot()
    def _invertNumber(self):
        displaytext = self.display.text()

        if not isValidNumber(displaytext):
            return
        
        number = convertToNumber(displaytext) * -1
        self.display.setText(str(number))
    
    @Slot()
    def _insertToDisplay(self,text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return
        
        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation =  self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self,text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if not isValidNumber(displayText) and self._left is None:
            self._showError("voce nao digitou nada.")
            return
        
        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f"{self._left} {self._op}??"

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError("sem nada para direita")
            return
        
        self._right = convertToNumber(displayText)
        self.equation= f"{self._left} {self._op} {self._right}"
        result = "error"
        try:
            if "^" in self.equation and isinstance(self._left, int | float):
                result = pow(self._left,self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError("is not divisible by zero")

        except OverflowError:
            self._showError("numero muito grande")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None
        self.display.setFocus()

        if self._left == "error":
            self._left = None


    @Slot()
    def _backSpace(self):
        self.display.backspace()
        self.display.setFocus()

    def _showError(self,text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.setStandardButtons(msgBox.StandardButton.Close)
        msgBox.exec()


        