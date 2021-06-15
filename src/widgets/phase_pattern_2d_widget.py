import sys

import pyqtgraph as pg
from PyQt5 import QtWidgets
from matplotlib import cm
import numpy as np


class PhasePattern2dWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._parent = parent
        self.vbox = QtWidgets.QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', 'φ', "°")
        self.plot_widget.setLabel('left', 'θ', "°")
        self.plot_widget.getPlotItem().getAxis('bottom').enableAutoSIPrefix(False)
        self.plot_widget.getPlotItem().getAxis('left').enableAutoSIPrefix(False)
        self.plot_widget.scene().sigMouseClicked.connect(self._mouse_clicked)
        self.vbox.addWidget(self.plot_widget)
        self.setLayout(self.vbox)

        self.img = None
        self.current_scale = [1, 1]
        self.currentMove = [0, 0]
        self.cross = None
        self.current_position = None

    def plot(self, results, log_scale):
        if self.img is None:
            self.img = pg.ImageItem()
            self.plot_widget.addItem(self.img)
        self._adjuct_color_map(log_scale)
        self.img.setImage(results['DNA'])

        fi_min, fi_max, theta_min, theta_max = results['limits_deg']
        scale_x = (fi_max - fi_min) / self.img.width()
        scale_y = (theta_max - theta_min) / self.img.height()
        if self.current_scale[0] != 0 and self.current_scale[1] != 0:
            self.img.scale(scale_x/self.current_scale[0], scale_y/self.current_scale[1])
            self.current_scale = [scale_x, scale_y]
            self.img.moveBy(fi_min - self.currentMove[0], theta_min - self.currentMove[1])
            self.currentMove = [fi_min, theta_min]

        self.plot_widget.setLimits(xMin=fi_min, xMax=fi_max, yMin=theta_min, yMax=theta_max)
        self.plot_widget.setRange(xRange=(fi_min, fi_max), yRange=(theta_min, theta_max))
        self.current_position = {'fi': np.degrees(results['fi_s']), 'theta': np.degrees(results['theta_s'])}
        self._plot_cross()

    def _adjuct_color_map(self, log_scale):
        if not log_scale:
            colormap = cm.get_cmap("jet")
            colormap._init()
            lut = (colormap._lut * 255).view(np.ndarray)
        else:
            pos = np.exp(np.linspace(-5, 0, 10))
            color = np.empty((10, 4), dtype=np.ubyte)
            color[:, :3] = np.linspace(0, 255, 10).reshape(10, 1)
            color[:, 3] = 255
            colormap = pg.ColorMap(pos, color)
            lut = colormap.getLookupTable(alpha=False)
        self.img.setLookupTable(lut)

    def _mouse_clicked(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(evt.scenePos())
        fi_deg, theta_deg = mouse_point.x(), mouse_point.y()
        self.current_position = {'fi': fi_deg, 'theta': theta_deg}
        self._parent.plot_slices()
        self._plot_cross()

    def _plot_cross(self):
        if self.cross is None:
            self.cross = self.plot_widget.plot([self.current_position['fi']], [self.current_position['theta']],
                                               symbol='+', pen=pg.mkPen(color='r'))
        else:
            self.cross.setData([self.current_position['fi']], [self.current_position['theta']])