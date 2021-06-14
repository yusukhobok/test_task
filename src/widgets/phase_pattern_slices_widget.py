import pyqtgraph as pg
from PyQt5 import QtWidgets

class PhasePatternSlicesWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.vbox = QtWidgets.QVBoxLayout()
        self.plot_widget_fi = pg.PlotWidget()
        self.plot_widget_fi.setLabel('bottom', 'φ', "°")
        self.plot_widget_fi.setLabel('left', 'G', "")
        self.plot_widget_fi.getPlotItem().getAxis('bottom').enableAutoSIPrefix(False)
        self.plot_widget_fi.getPlotItem().getAxis('left').enableAutoSIPrefix(False)
        self.plot_widget_fi.scene().sigMouseClicked.connect(self.mouse_clicked_fi)
        self.plot_widget_theta = pg.PlotWidget()
        self.plot_widget_theta.setLabel('bottom', 'θ', "°")
        self.plot_widget_theta.setLabel('left', 'G', "")
        self.plot_widget_theta.getPlotItem().getAxis('bottom').enableAutoSIPrefix(False)
        self.plot_widget_theta.getPlotItem().getAxis('left').enableAutoSIPrefix(False)
        self.plot_widget_theta.scene().sigMouseClicked.connect(self.mouse_clicked_theta)
        self.vbox.addWidget(self.plot_widget_fi)
        self.vbox.addWidget(self.plot_widget_theta)
        self.setLayout(self.vbox)

    def mouse_clicked_fi(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(evt.scenePos())
        x = mouse_point.x()
        y = mouse_point.y()
        btn = evt.button()
        print(x, y)

    def mouse_clicked_theta(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(evt.scenePos())
        x = mouse_point.x()
        y = mouse_point.y()
        btn = evt.button()
        print(x, y)