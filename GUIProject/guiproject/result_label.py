from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class ResultLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Arial', 180))
        self.setAlignment(Qt.AlignCenter)

    def set_number(self, number: int):
        self.setText(str(number))

    def clear(self):
        self.setText('')
