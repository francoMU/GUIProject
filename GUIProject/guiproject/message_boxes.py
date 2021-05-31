"""
Collection of factory methods for message boxes
"""

from PyQt5.QtWidgets import QMessageBox


def create_error_message_box(text: str = None,
                             information_text: str = None,
                             title: str = "Error") -> QMessageBox:
    """
    Create an error message that has to be just has to be executated

    :param text: message of error message box
    :param information_text: information text
    :param title: title of what happened
    :return: `QMessageBox` instance is return
    """

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    if text is not None:
        msg.setText(text)

    if information_text is not None:
        msg.setInformativeText(information_text)

    msg.setWindowTitle(title)

    return msg
