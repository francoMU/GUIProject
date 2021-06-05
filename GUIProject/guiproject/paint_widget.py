import numpy as np
from PIL import Image
from PIL.Image import LANCZOS
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygon
from PyQt5.QtWidgets import (QWidget)


class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.x_limit = (0, 300)
        self.y_limit = (0, 300)

        self.radius_size = 5

        self.setGeometry(0, 0, 300, 300)

        self.points = QPolygon()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x_position = event.x()
            y_position = event.y()

            if self.is_in_widget(x_position, y_position):
                self.points << event.pos()
                self.update()

    def is_in_widget(self, x_point, y_point):
        if x_point >= self.x_limit[0] and x_point < self.x_limit[1]:
            if y_point >= self.y_limit[0] and y_point < self.y_limit[1]:
                return True

    def mouseMoveEvent(self, event):

        x_position = event.x()
        y_position = event.y()

        if self.is_in_widget(x_position, y_position):
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
            qp.drawEllipse(self.points.point(i), self.radius_size,
                           self.radius_size)

    def get_image_matrix(self):

        image_matrix = np.zeros((self.x_limit[1], self.y_limit[1]),
                                dtype=np.uint8)

        radius_points = self.list_of_points(self.radius_size)

        for i in range(self.points.count()):
            point = self.points.point(i)

            y = int(299 - point.y())
            x = int(point.x())

            central_point = np.array((x, y))

            points = central_point + radius_points

            for i_x, i_y in points:

                if self.is_in_widget(i_x, i_y):
                    image_matrix[i_x, i_y] = np.uint8(255)

        img = Image.fromarray(image_matrix)

        resized_image = img.resize((28, 28), LANCZOS)
        resized_image.save('my.png')

    @staticmethod
    def list_of_points(radius):

        points = []

        for x in range(- radius, radius + 1):
            for y in range(- radius, radius + 1):
                if (x * x + y * y <= radius * radius):
                    points.append((x, y))

        return np.array(points, dtype=int)

    def clear(self):

        for i in range(self.points.count()):
            point = self.points.point(i)

            print(point.y(), point.x())

        self.points.clear()
        self.update()
