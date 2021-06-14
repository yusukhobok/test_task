import pyqtgraph as pg
from PyQt5 import QtWidgets

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

    def mouseClicked(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(evt.scenePos())
        x = mouse_point.x()
        y = mouse_point.y()
        btn = evt.button()
        print(x, y)