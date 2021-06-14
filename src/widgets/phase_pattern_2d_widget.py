import pyqtgraph as pg
from PyQt5 import QtWidgets
from matplotlib import cm
import numpy as np

class PhasePattern2dWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
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

        scale_x = (phase_pattern.fi_max - phase_pattern.fi_min) / self.img.width()
        scale_y = (phase_pattern.theta_max - phase_pattern.theta_min) / self.img.height()
        if self.current_scale[0] != 0 and self.current_scale[1] != 0:
            self.img.scale(scale_x/self.current_scale[0], scale_y/self.current_scale[1])
            self.current_scale = [scale_x, scale_y]
            self.img.moveBy(phase_pattern.fi_min - self.currentMove[0], phase_pattern.theta_min - self.currentMove[1])
            self.currentMove = [phase_pattern.fi_min, phase_pattern.theta_min]

        self.plot_widget.setLimits(xMin = phase_pattern.fi_min, xMax = phase_pattern.fi_max, yMin = phase_pattern.theta_min, yMax = phase_pattern.theta_max)
        self.plot_widget.setRange(xRange = (phase_pattern.fi_min, phase_pattern.fi_max), yRange = (phase_pattern.theta_min, phase_pattern.theta_max))



    # limits = [phase_pattern.fi_min, phase_pattern.fi_max, phase_pattern.theta_max, phase_pattern.theta_min]
    # limits_deg = np.rad2deg(limits)
    # plt.imshow(phase_pattern.DNA, extent=limits_deg)
    # plt.colorbar()

    def _adjuct_color_map(self):
        colormap = cm.get_cmap("jet")
        colormap._init()
        lut = (colormap._lut * 255).view(np.ndarray)
        self.img.setLookupTable(lut)

    def mouseClicked(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(evt.scenePos())
        x = mouse_point.x()
        y = mouse_point.y()
        btn = evt.button()
        print(x, y)