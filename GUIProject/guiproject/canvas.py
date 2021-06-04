"""
Module containing handle all the details of talking to user interface toolkits
"""
import matplotlib

matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from guiproject.mnist import training_images


class MplCanvas(FigureCanvas):
    """
    Canvas for plotting the points of a fit
    """

    def __init__(self, parent=None, width=5, height=5):
        self._figure = Figure(figsize=(width, height))

        self.axes = self._figure.add_subplot()

        images = training_images()

        self.axes.imshow(255 - images[0, :, :], aspect='equal', cmap='gray')
        self.axes.set_axis_off()
        self._figure.tight_layout()

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
