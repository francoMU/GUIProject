"""
Module containing handle all the details of talking to user interface toolkits
"""
import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """
    Canvas for plotting the points of a fit
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self._figure = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self._figure.add_subplot()

        self.axes.set_ylabel('Energy')
        self.axes.set_xlabel('Delta')

        super().__init__(self._figure)

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
