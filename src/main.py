import os
import sys

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication

from interface import MainWindow


if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    pg.setConfigOption('background', 'w')
    os.environ['ETS_TOOLKIT'] = 'qt4'

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()