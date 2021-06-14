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
        self.plot_widget.scene().sigMouseClicked.connect(self.mouseClicked)
        self.vbox.addWidget(self.plot_widget)
        self.setLayout(self.vbox)

        self.img = None
        self.current_scale = [1, 1]
        self.currentMove = [0, 0]

    def plot(self, phase_pattern):
        if self.img is None:
            self.img = pg.ImageItem()
            self._adjuct_color_map()
            self.plot_widget.addItem(self.img)
        self.img.setImage(phase_pattern.DNA)

        fi_min, fi_max, theta_min, theta_max = phase_pattern.limits_to_degrees()
        scale_x = (fi_max - fi_min) / self.img.width()
        scale_y = (theta_max - theta_min) / self.img.height()
        if self.current_scale[0] != 0 and self.current_scale[1] != 0:
            self.img.scale(scale_x/self.current_scale[0], scale_y/self.current_scale[1])
            self.current_scale = [scale_x, scale_y]
            self.img.moveBy(fi_min - self.currentMove[0], theta_min - self.currentMove[1])
            self.currentMove = [fi_min, theta_min]

        self.plot_widget.setLimits(xMin = fi_min, xMax = fi_max, yMin = theta_min, yMax = theta_max)
        self.plot_widget.setRange(xRange = (fi_min, fi_max), yRange = (theta_min, theta_max))

    def _adjuct_color_map(self):
        colormap = cm.get_cmap("jet")
        colormap._init()
        lut = (colormap._lut * 255).view(np.ndarray)
        self.img.setLookupTable(lut)

    def mouseClicked(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(evt.scenePos())
        fi_deg = mouse_point.x()
        theta_deg = mouse_point.y()
        self._parent.plot_slices(fi_deg, theta_deg)