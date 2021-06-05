"""
Module containing handle all the details of talking to user interface toolkits
"""
import matplotlib

import numpy as np

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """
    Canvas for plotting the points of a fit
    """

    def __init__(self, parent=None):
        self._figure = Figure()

        self.axes = self._figure.add_subplot()
        self.axes.set_axis_off()
        self._figure.tight_layout(pad=1.00, h_pad=0, w_pad=0)

        super().__init__(self._figure)

    def update_image(self, image):

        if np.allclose(image, 0):
            self.clear()
        else:
            self.axes.imshow(255 - image[:, :], aspect='equal', cmap='gray')
            self.axes.set_axis_off()
        self._figure.tight_layout(pad=1.00, h_pad=0, w_pad=0)

    def clear(self):
        self.axes.clear()
        self.axes.set_axis_off()
        self.draw()

    @property
    def figure(self):
        """
        Get figure instance
        :return: figure instance
        """
        return self._figure

    @figure.setter
    def figure(self, obj: Figure) -> None:
        """
        Set the figure instance
        :param obj: figure instance
        """
        self._figure = obj
