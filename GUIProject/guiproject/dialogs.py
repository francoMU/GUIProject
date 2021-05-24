from importlib import resources

import numpy as np
import pkg_resources
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QWheelEvent
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QGridLayout, \
    QWidgetItem
from guiproject.utils import find_whitespaces


class AboutDialog(QDialog):
    """Create the necessary elements to show helpful text in a dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super().__init__(parent)

        self.setWindowTitle('About')
        help_icon = pkg_resources.resource_filename('guiproject.images',
                                                    'ic_help_black_48dp_1x.png')

        self.default_width = 300
        self.default_height = 200

        self.font_size = 12

        self.font = 'Arial'

        self.setWindowIcon(QIcon(help_icon))

        self.resize(self.default_width,
                    self.default_height)

        license_text = self.get_license_text()

        self.split_lines(license_text)

        license = QLabel(license_text)
        license.setAlignment(Qt.AlignCenter)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignVCenter)

        self.sub_layout = QGridLayout()
        self.sub_layout.setColumnStretch(0, 4)
        self.sub_layout.setColumnStretch(1, 4)

        author = QLabel('Franco Peter Moitzi')
        author.setAlignment(Qt.AlignCenter)

        name = QLabel('Name:')
        name.setAlignment(Qt.AlignCenter)

        github = QLabel('francoMU')
        github.setAlignment(Qt.AlignCenter)

        github_name = QLabel("Github Name:")
        github_name.setAlignment(Qt.AlignCenter)

        self.sub_layout.addWidget(name, 0, 0)
        self.sub_layout.addWidget(author, 0, 1)

        self.sub_layout.addWidget(github_name, 1, 0)
        self.sub_layout.addWidget(github, 1, 1)

        self.main_layout.addLayout(self.sub_layout)
        self.main_layout.addWidget(license)

        self.setLayout(self.main_layout)
        self.change_font_size(self.font_size)

    def get_license_text(self):
        return resources.read_text('guiproject.data',
                                   'license.txt')

    def split_lines(self, text: str, width=120):
        """This method splits lines after certain number of characters"""

        lines = text.splitlines()

        for line in lines:
            indices = list(find_whitespaces(line))

            max(filter(lambda x: x < , indices))

            print(indices)

        # font.setFixedPitch(True)

    def change_font_size(self, size: float):
        """Changes all font sizes"""
        for i in range(self.main_layout.count()):

            widget_item = self.main_layout.itemAt(i)

            if isinstance(widget_item, QWidgetItem):
                item = self.main_layout.itemAt(i).widget()
                item.setFont(QFont(self.font, size))

            if isinstance(widget_item, QGridLayout):
                for j in range(widget_item.count()):
                    item = widget_item.itemAt(j).widget()
                    item.setFont(QFont(self.font, size))

    def wheelEvent(self, event: QWheelEvent):
        delta = np.sign(event.angleDelta().y())
        self.font_size += delta
        self.change_font_size(self.font_size)

    def resizeEvent(self, event):
        print(self.size())
        print("fuck")
