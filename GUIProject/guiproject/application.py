import sys

import pkg_resources
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QFileDialog,
                             QMainWindow, QToolBar, QWidget, QVBoxLayout)
from guiproject.canvas import MplCanvas
from guiproject.dialogs import AboutDialog
from guiproject.message_boxes import create_error_message_box
from guiproject.mixins import LoggerMixin
from guiproject.selectable_points import DataSchema
from monty.serialization import loadfn


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))


class ApplicationWindow(QMainWindow, LoggerMixin):
    """Create the main window that stores all of the widgets necessary for
    the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super(ApplicationWindow, self).__init__(parent)

        self.resize(1024, 768)
        self.setWindowTitle('Template')

        window_icon = pkg_resources.resource_filename('guiproject.images',
                                                      'ic_insert_drive_file_black_48dp_1x.png')

        self.data = None

        self.setWindowIcon(QIcon(window_icon))

        self.layout = QVBoxLayout()

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.menu_bar = self.menuBar()
        self.about_dialog = AboutDialog()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)

        self.file_menu()
        self.help_menu()

        self.tool_bar_items()

        self.central_canvas()

    def central_canvas(self):
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        x_data = [0, 1, 2, 3, 4]
        y_data = [0, 1, 20, 3, 40]

        for x, y in zip(x_data, y_data):
            self.sc.axes.plot(x,
                              y,
                              "ro",
                              picker=True,
                              pickradius=5)

        # https: // matplotlib.org / stable / users / event_handling.html

        # sc.mpl_connect('button_press_event', onclick)

        self.sc.mpl_connect('pick_event', self.onpick)

        self.layout.addWidget(self.sc)

    def onpick(self, event):
        thisline = event.artist
        print(type(thisline))

        print(thisline.get_color())

        thisline.set_color("blue")

        self.sc.draw()

        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = tuple(zip(xdata[ind], ydata[ind]))
        print('onpick points:', points)

    def file_menu(self):
        """Create a file submenu with an Open File item that opens a file
        dialog."""
        self.file_sub_menu = self.menu_bar.addMenu('File')

        self.open_action = QAction('Open File', self)
        self.open_action.setStatusTip('Open a file into Template.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.exit_action = QAction('Exit Application', self)
        self.exit_action.setStatusTip('Exit the application.')
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(lambda: QApplication.quit())

        self.file_sub_menu.addAction(self.open_action)
        self.file_sub_menu.addAction(self.exit_action)

    def help_menu(self):
        """Create a help submenu with an About item tha opens an about
        dialog."""
        self.help_sub_menu = self.menu_bar.addMenu('Help')

        self.about_action = QAction('About', self)
        self.about_action.setStatusTip('About the application.')
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(lambda: self.about_dialog.exec_())

        self.help_sub_menu.addAction(self.about_action)

    def tool_bar_items(self):
        """Create a tool bar for the main window."""
        self.tool_bar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
        self.tool_bar.setMovable(False)

        open_icon = pkg_resources.resource_filename('guiproject.images',
                                                    'ic_open_in_new_black_48dp_1x.png')
        tool_bar_open_action = QAction(QIcon(open_icon), 'Open File', self)
        tool_bar_open_action.triggered.connect(self.open_file)

        self.tool_bar.addAction(tool_bar_open_action)

    def open_file(self):
        """Open a QFileDialog to allow the user to open a file into the
        application."""
        filename, selected_filter = QFileDialog.getOpenFileName(self,
                                                                'Open File',
                                                                '',
                                                                "Text files "
                                                                "(*.json)")

        try:
            raw_data = loadfn(filename)

            schema = DataSchema()
            data = schema.load(raw_data)
            self.data = data
        except BaseException as exc:
            self.logger.error("A problem with loading the file occured", exc)
            message_box = create_error_message_box("File not valid",
                                                   "Please open a different on")
            message_box.exec()


def main():
    application = QApplication(sys.argv)
    window = ApplicationWindow()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
