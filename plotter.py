from ast import literal_eval
import Testing
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QApplication,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
# Plotting imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
# Utilities imports
import numpy as np
import sys
import re

words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    '/',
    '+',
    '*',
    '^',
    '-',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]

rep = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**'
}


def getFunction(expr):
    for word in re.findall('[a-zA-Z_]+', expr):
        if word not in words:
            raise ValueError(
                "Only functions of 'x' are allowed.\ne.g., 5*x^3 + 2/x - 1"
            )
    for char, newChar in rep.items():
        expr = expr.replace(char, newChar)

    if "x" not in expr:
        expr = expr + "+x*0"

    def evaluate(x):
        try:
            return eval(expr)
        except ZeroDivisionError:
            raise ValueError("error zero diveded")

    return evaluate


class Plotter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Plotter")

        QApplication.setFont(QFont("Calibri", 12))

        self.view = FigureCanvas(Figure(figsize=(30, 30)))
        self.axes = self.view.figure.subplots()

        self.mn = QLineEdit()
        self.mnLabel = QLabel(text="Min of X:")

        self.mx = QLineEdit()
        self.mxLabel = QLabel(text="Max of X:")

        self.funField = QLineEdit()
        self.funLabel = QLabel(text="Function: ")
        self.submit = QPushButton(text="plot")

        # setting all the layout wedget
        FunLayout = QHBoxLayout()
        FunLayout.addWidget(self.funLabel)
        FunLayout.addWidget(self.funField)
        FunLayout.addWidget(self.submit)

        RangeLayout = QHBoxLayout()
        RangeLayout.addWidget(self.mnLabel)
        RangeLayout.addWidget(self.mn)
        RangeLayout.addWidget(self.mxLabel)
        RangeLayout.addWidget(self.mx)

        WindowLayout = QVBoxLayout()
        WindowLayout.addWidget(self.view)
        WindowLayout.addLayout(FunLayout)
        WindowLayout.addLayout(RangeLayout)
        self.setLayout(WindowLayout)

        self.error_dialog = QMessageBox()
        self.mn.setText("1.0")
        self.mx.setText("100.0")

        self.submit.clicked.connect(lambda _: self.action())


    def action(self):
        mn = self.mn.text()
        mx = self.mx.text()
        function = self.funField.text()
        if mn == "" or mx == "" or function == "":
            self.error_dialog.setWindowTitle(" Fields Error!")
            self.error_dialog.setText("The fields musn't be empty")
            self.error_dialog.show()
            return

        mn = float(mn)
        mx = float(mx)
        if mn > mx:
            self.error_dialog.setWindowTitle(" limits Error!")
            self.error_dialog.setText("Error in the X Boundry")
            self.error_dialog.show()
            return

        x = np.linspace(mn, mx)

        try:
            y = getFunction(function)(x)
        except SyntaxError as error :
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText(str(error))
            self.error_dialog.show()
            return
        except RuntimeWarning as error:
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText(str(error))
            self.error_dialog.show()
            return

        self.axes.clear()
        self.axes.plot(x, y)
        self.view.draw()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Plotter()
    window.show()
    sys.exit(app.exec_())
