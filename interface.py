from PyQt5 import QtCore, QtWidgets

from calculations import PhasePattern
from thread import Operation
from widgets.settings_widget import SettingsWidget
from widgets.phase_pattern_2d_widget import PhasePattern2dWidget
from widgets.phase_pattern_3d_widget import PhasePattern3dWidget
from widgets.phase_pattern_slices_widget import PhasePatternSlicesWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.phase_pattern = PhasePattern()
        self.title = "Диаграмма направленности фазированной антенной решетки"

        self.setWindowTitle(self.title)
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
        self.operation = Operation(self)
        self.recalculate(first_run=True)

    def recalculate(self, first_run=False):
        """Расчет ДНА (запускается в отдельном потоке)"""
        self.setWindowTitle(f"{self.title} (РАСЧЕТ...)")
        self.settings_widget.setEnabled(False)
        options = self.settings_widget.to_dict()
        self.operation.set_func(self.phase_pattern.refresh, options)
        self.operation.set_finish_function(self.after_calculation, self, first_run, options)
        self.operation.start()

    def after_calculation(self, result, first_run, options):
        if first_run or result:
            widgets = (self.phase_pattern_2d_widget, self.phase_pattern_3d_widget, self.phase_pattern_slices_widget)
            for widget in widgets:
                widget.setEnabled(False)
            self.refresh_plots()
            self.after_refresh_plots()

    def refresh_plots(self):
        """Перерисовка диаграмм после расчета ДНА"""
        self.plot_2d()
        self.plot_3d()
        self.plot_slices()

    def after_refresh_plots(self):
        widgets = (self.phase_pattern_2d_widget, self.phase_pattern_3d_widget, self.phase_pattern_slices_widget)
        for widget in widgets:
            widget.setEnabled(True)
        self.settings_widget.setEnabled(True)
        self.setWindowTitle(self.title)

    def plot_2d(self):
        """Отображение двумерной цветовой карты"""
        self.phase_pattern_2d_widget.plot(self.phase_pattern.results)

    def plot_3d(self):
        """3D отображение ДНА"""
        self.phase_pattern_3d_widget.plot(self.phase_pattern.results)

    def plot_slices(self):
        """Отображение двух срезов (по азимуту и по возвышению)"""
        fi_deg = self.phase_pattern_2d_widget.current_position['fi']
        theta_deg = self.phase_pattern_2d_widget.current_position['theta']
        slice_fi_deg, slice_theta_deg = self.phase_pattern.get_slices(fi_deg, theta_deg)
        self.phase_pattern_slices_widget.plot_slices(fi_deg, theta_deg, slice_fi_deg, slice_theta_deg,
                                                     self.phase_pattern.results)



