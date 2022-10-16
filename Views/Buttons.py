from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton

from Servise.Variable import minSizeButton, maxSizeButton


class Button(QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        self.setMaximumSize(minSizeButton)
        self.setMaximumSize(maxSizeButton)
        self.setText(text)
