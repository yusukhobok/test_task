import sys

import numpy as np
import pyqtgraph as pg
# import qdarkstyle
from matplotlib import image
from PyQt5 import QtCore, QtWidgets, QtGui



from calculations import PhasePattern
import matplotlib.pyplot as plt
import numpy as np

from PyQt5.QtWidgets import QApplication

from interface import MainWindow



def test():
    options = {
        "fi_s_deg": 30.,
        "theta_s_deg": 20.,
        "fi_0_deg": 10.,
        "theta_0_deg": 10.,
        "fi_count": 10000,
        "theta_count": 10000,
    }
    


    phase_pattern = PhasePattern(options)
    phase_pattern.calc_DNA()
    phase_pattern.calc_cartesian()

    # limits = [phase_pattern.fi_min, phase_pattern.fi_max, phase_pattern.theta_max, phase_pattern.theta_min]
    # limits_deg = np.rad2deg(limits)
    # plt.imshow(phase_pattern.DNA, extent=limits_deg)
    # plt.colorbar()

    # delta_fi = phase_pattern.fi_array[1] - phase_pattern.fi_array[0]
    # delta_theta = phase_pattern.theta_array[1] - phase_pattern.theta_array[0]
    # index_fi = int((phase_pattern.fi_s - phase_pattern.fi_min) // delta_fi)
    # index_theta = int((phase_pattern.theta_s - phase_pattern.theta_min) // delta_theta)
    # plt.plot(phase_pattern.fi_array, phase_pattern.DNA[:,index_theta])
    # plt.plot(phase_pattern.theta_array, phase_pattern.DNA[index_theta, :])

    # from mpl_toolkits.mplot3d import Axes3D
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.plot_trisurf(phase_pattern.cartesian['x'], phase_pattern.cartesian['y'], phase_pattern.cartesian['z'],
    #                 triangles=phase_pattern.cartesian['tri'].triangles, cmap=plt.cm.Spectral)

    plt.show()


if __name__ == "__main__":
    QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    pg.setConfigOption('background', 'w')

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    app.exec()