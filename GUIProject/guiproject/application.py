"""
Module containing the main application
"""

import sys

import numpy as np
import pkg_resources
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QMainWindow,
                             QToolBar, QWidget, QVBoxLayout,
                             QPushButton, QHBoxLayout, QFileDialog,
                             QDialog)
from guiproject.canvas import MplCanvas
from guiproject.dialogs import AboutDialog
from guiproject.message_boxes import create_error_message_box
from guiproject.mixins import LoggerMixin
from guiproject.paint_widget import PaintWidget
from guiproject.result_label import ResultLabel
from keras.models import load_model


class ApplicationWindow(QMainWindow, LoggerMixin):
    """Create the main window that stores all of the widgets necessary for
    the application."""

    def __init__(self, parent=None):
        """Initialize the components of the main window."""
        super(ApplicationWindow, self).__init__(parent)

        self.setWindowTitle('CNN Digit Predictor')

        self.setFixedSize(1110, 405)

        window_icon = pkg_resources.resource_filename('guiproject.images',
                                                      'ic_insert_drive_file_black_48dp_1x.png')

        self.data = None

        self.setWindowIcon(QIcon(window_icon))

        self.menu_bar = self.menuBar()
        self.about_dialog = AboutDialog()

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)

        self.file_menu()
        self.help_menu()

        self.tool_bar_items()

        # Main Layout

        self.layout = QHBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Painter application

        self.painter_label = PaintWidget()
        self.painter_label.setFixedSize(300, 300)
        self.painter_label.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.painter_label)

        # Button
        self.sub_layout_1 = QVBoxLayout()
        self.layout.addLayout(self.sub_layout_1)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.painter_label.clear)

        self.sub_layout_1.addWidget(self.clear_button)

        self.convert_button = QPushButton('Convert')
        self.sub_layout_1.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.update_canvas)

        # Converted
        self.converter_label = MplCanvas()
        self.converter_label.setFixedSize(300, 300)
        self.converter_label.setStyleSheet("border: 1px solid black;")
        self.converter_label.draw()
        self.layout.addWidget(self.converter_label)

        self.clear_button.clicked.connect(self.converter_label.clear)

        # Button
        self.sub_layout_2 = QVBoxLayout()
        self.layout.addLayout(self.sub_layout_2)

        self.predict_button = QPushButton('Predict')
        self.sub_layout_2.addWidget(self.predict_button)

        self.predict_button.clicked.connect(self.update_predict)

        # Predicted Number
        self.result_label = ResultLabel()
        self.result_label.setFixedSize(300, 300)
        self.result_label.setStyleSheet("border: 1px solid black;")
        self.result_label.clear()
        self.layout.addWidget(self.result_label)

        self.clear_button.clicked.connect(self.result_label.clear)

        self.image = None

        # load model
        resolved_filename = pkg_resources.resource_filename('guiproject.data',
                                                            'full_model.h5')

        self.model = load_model(resolved_filename, compile=True)

    def update_canvas(self):
        self.image = self.painter_label.get_image_matrix()

        self.converter_label.update_image(self.image)

        self.converter_label.draw()

    def update_predict(self):
        if self.image is not None:
            image = np.array(self.image).astype('float32').reshape(-1, 28,
                                                                   28, 1)

            image = image / 255.0

            result = self.model.predict(image).argmax()

            self.result_label.set_number(result)

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
        dialog = QFileDialog(parent=self)
        dialog.setWindowTitle('Open keras model')
        dialog.setDirectory(QDir.currentPath())
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])

            try:
                self.model = load_model(file_full_path, compile=True)
            except OSError:
                error_box = create_error_message_box("Wrong file",
                                                     "This file is not a "
                                                     "valid model file"
                                                     )
                error_box.exec()


def main():
    application = QApplication(sys.argv)
    window = ApplicationWindow()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
