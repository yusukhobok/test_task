from PyQt5 import QtWidgets

import pyqtgraph as pg
from pyqtgraph import opengl

import os
os.environ['ETS_TOOLKIT'] = 'qt4'


class PhasePattern3dWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.plot_widget = opengl.GLViewWidget()
        self.plot_widget.setBackgroundColor(250, 250, 250)
        self.axisItem = opengl.GLAxisItem()
        self.vbox.addWidget(self.plot_widget)
        self.setLayout(self.vbox)
        self.showMaximized()