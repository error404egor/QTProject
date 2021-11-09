# This Python file uses the following encoding: utf-8
import os
import sys
import PyQt5
from PyQt5.QtGui import QIcon, QPixmap
from TEST import test

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtCore import QFile, QSize, Qt
from PyQt5 import uic
from PyQt5 import *


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        uic.loadUi("form.ui", self)
        self.logo.setPixmap(QPixmap("./IMG/logo.png").scaled(201, 71, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.reload.setIcon(QIcon("./IMG/reload.svg"))
        test(self, self.inFreezerLayout)
        test(self, self.inFreezerLayout)
        test(self, self.inFreezerLayout)
        test(self, self.inFreezerLayout)
        test(self, self.inFreezerLayout)



if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
