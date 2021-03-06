import pyqtgraph as pg
from PyQt5 import QtWidgets
import numpy as np


class PhasePatternSlicesWidget(QtWidgets.QWidget):
    """Виджет с отображением двух срезов (по азимуту и по возвышению)"""

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.plot_widget_fi = pg.PlotWidget()
        self.plot_widget_theta = pg.PlotWidget()
        self.line_fi = None
        self.line_theta = None
        for plot_widget in (self.plot_widget_fi, self.plot_widget_theta):
            plot_widget.setLabel('bottom', 'θ', '°')
            plot_widget.setLabel('left', 'G', '')
            plot_widget.getPlotItem().getAxis('bottom').enableAutoSIPrefix(False)
            plot_widget.getPlotItem().getAxis('left').enableAutoSIPrefix(False)
            self.vbox.addWidget(plot_widget)
        self.setLayout(self.vbox)

    def plot_slices(self, fi_deg, theta_deg, slice_fi_deg, slice_theta_deg, results):
        fi_min, fi_max, theta_min, theta_max = results['limits_deg']

        if self.line_fi is None:
            self.line_fi = self.plot_widget_fi.plot(np.degrees(results['fi_array']), slice_fi_deg,
                                                    pen=pg.mkPen(color='b'))
        else:
            self.line_fi.setData(np.degrees(results['fi_array']), slice_fi_deg)
        self.plot_widget_fi.setTitle(f"θ = {theta_deg:.2f}°")
        self.plot_widget_fi.setLimits(xMin=fi_min, xMax=fi_max, yMin=slice_fi_deg.min(), yMax=slice_fi_deg.max())
        self.plot_widget_fi.getPlotItem().enableAutoRange()
        self.plot_widget_fi.setLogMode(False, results['log_scale'])

        if self.line_theta is None:
            self.line_theta = self.plot_widget_theta.plot(np.degrees(results['theta_array']), slice_theta_deg,
                                                          pen=pg.mkPen(color='b'))
        else:
            self.line_theta.setData(np.degrees(results['theta_array']), slice_theta_deg)
        self.plot_widget_theta.setTitle(f"φ = {fi_deg:.2f}°")
        self.plot_widget_theta.setLimits(xMin=theta_min, xMax=theta_max, yMin=slice_theta_deg.min(),
                                         yMax=slice_theta_deg.max())
        self.plot_widget_theta.getPlotItem().enableAutoRange()
        self.plot_widget_theta.setLogMode(False, results['log_scale'])
