from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon
from PyQt5.QtWidgets import (QWidget)


class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 300, 300)

        self.points = QPolygon()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(event.pos())
            self.points << event.pos()
            self.update()

    def mouseMoveEvent(self, event):

        print(event.pos())

        self.points << event.pos()
        self.update()

    def paintEvent(self, ev):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 5)
        brush = QBrush(Qt.black)
        qp.setPen(pen)
        qp.setBrush(brush)
        for i in range(self.points.count()):
            qp.drawEllipse(self.points.point(i), 5, 5)

    def clear(self):

        for i in range(self.points.count()):
            point = self.points.point(i)

            print(point.y(), point.x())

        self.points.clear()
        self.update()
