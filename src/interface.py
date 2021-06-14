from PyQt5 import QtCore, QtWidgets

from widgets.settings_widget import SettingsWidget
from widgets.phase_pattern_2d_widget import PhasePattern2dWidget
from widgets.phase_pattern_3d_widget import PhasePattern3dWidget
from widgets.phase_pattern_slices_widget import PhasePatternSlicesWidget

from calculations import PhasePattern


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Диаграмма направленности фазированной антенной решетки")
        self.setWindowFlags(QtCore.Qt.Window)

        self.settings_widget = SettingsWidget(self)
        self.phase_pattern_2d_widget = PhasePattern2dWidget(self)
        self.phase_pattern_3d_widget = PhasePattern3dWidget(self)
        self.phase_pattern_slices_widget = PhasePatternSlicesWidget(self)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.settings_widget, 0, 0)
        self.grid.addWidget(self.phase_pattern_3d_widget, 0, 1)
        self.grid.addWidget(self.phase_pattern_slices_widget, 1, 0)
        self.grid.addWidget(self.phase_pattern_2d_widget, 1, 1)

        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.grid)
        self.showMaximized()

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

        self.phase_pattern = PhasePattern(self.settings_widget.to_dict())
        self.log_scale = False

    def refresh(self):
        options = self.settings_widget.to_dict()
        self.phase_pattern.refresh(options)
        self.log_scale = options['log_scale']
        self.plot_2d()
        self.plot_3d()

    def plot_2d(self):
        self.phase_pattern_2d_widget.plot(self.phase_pattern, self.log_scale)

    def plot_3d(self):
        self.phase_pattern_3d_widget.plot(self.phase_pattern, self.log_scale)

    def plot_slices(self, fi_deg, theta_deg):
        slice_fi_deg, slice_theta_deg = self.phase_pattern.get_slices(fi_deg, theta_deg)
        self.phase_pattern_slices_widget.plot_slices(fi_deg, theta_deg, slice_fi_deg, slice_theta_deg,
                                                     self.phase_pattern, self.log_scale)

