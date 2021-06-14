import matplotlib.tri as mtri
import numpy as np


class PhasePattern:
    def __init__(self, options):
        self.fi_s = np.radians(30)
        self.theta_s = np.radians(20)
        self.fi_0 = np.radians(10)
        self.theta_0 = np.radians(10)
        self.fi_count = 10000
        self.theta_count = 10000

        self.l_main = 10
        self.l_side = 1

        self.fi_min = np.radians(-60)
        self.fi_max = np.radians(60)
        self.theta_min = np.radians(-50)
        self.theta_max = np.radians(50)


        self.fi_array = None
        self.theta_array = None
        self.fi_grid = None
        self.theta_grid = None

        self.DNA = None
        self.cartesian = None

        self.refresh(options)

    def refresh(self, options):
        self.fi_s = np.radians(options.get("fi_s_deg", 30))
        self.theta_s = np.radians(options.get("theta_s_deg", 20))
        self.fi_0 = np.radians(options.get("fi_0_deg", 10))
        self.theta_0 = np.radians(options.get("theta_0_deg", 10))
        self.fi_count = options.get("fi_count", 10000)
        self.theta_count = options.get("theta_count", 10000)
        self._fill_angle_arrays()
        self.calc_DNA()
        self.calc_cartesian()

    def _calc_l(self, fi, theta):
        L = np.empty((self.fi_count, self.theta_count))
        L.fill(self.l_side)
        cond1 = np.abs(fi - self.fi_s) < self.fi_0 / np.cos(self.fi_s)
        cond2 = np.abs(theta - self.theta_s) < self.theta_0 / np.cos(self.theta_s)
        L[cond1 & cond2] = self.l_main
        return L

    def _calc_G(self, fi, theta):
        frac1 = np.pi * (fi - self.fi_s) * np.cos(self.fi_s) / (2 * self.fi_0)
        frac2 = np.pi * (theta - self.theta_s) * np.cos(self.theta_s) / (2 * self.theta_0)
        L = self._calc_l(fi, theta)
        return np.abs(np.cos(frac1) * np.cos(frac2)) * L

    def _fill_angle_arrays(self):
        self.fi_array = np.linspace(self.fi_min, self.fi_max, self.fi_count)
        self.theta_array = np.linspace(self.theta_min, self.theta_max, self.theta_count)

    def calc_DNA(self):
        self.fi_grid, self.theta_grid = np.meshgrid(self.fi_array, self.theta_array)
        self.DNA = self._calc_G(self.fi_grid, self.theta_grid)

    def calc_cartesian(self):
        fi_gaps = len(self.fi_array) // 100
        if fi_gaps == 0:
            fi_gaps = 1
        theta_gaps = len(self.theta_array) // 100
        if theta_gaps == 0:
            theta_gaps = 1

        fi = self.fi_grid[::fi_gaps, ::theta_gaps].flatten()
        theta = self.theta_grid[::fi_gaps, ::theta_gaps].flatten()
        r = self.DNA[::fi_gaps, ::theta_gaps].flatten()

        x = r * np.sin(theta) * np.cos(fi)
        y = r * np.sin(theta) * np.sin(fi)
        z = r * np.cos(theta)
        tri = mtri.Triangulation(fi, theta)
        self.cartesian = {'x': x, 'y': y, 'z': z, 'tri': tri}




