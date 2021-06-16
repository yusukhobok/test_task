import matplotlib.tri
import numpy as np


class PhasePattern:
    DEFAULT_OPTIONS = {
            'fi_s_deg': 40,
            'theta_s_deg': 20,
            'fi_0_deg': 10,
            'theta_0_deg': 15,
            'fi_count': 1000,
            'theta_count': 1000,
            'l_main': 50,
            'l_side': 10,
            'fi_min_deg': -90,
            'fi_max_deg': 90,
            'theta_min_deg': -90,
            'theta_max_deg': 90,
            'fi_s_min_deg': -60,
            'fi_s_max_deg': 60,
            'theta_s_min_deg': -60,
            'theta_s_max_deg': 60,
            'fi_0_min_deg': 1,
            'fi_0_max_deg': 15,
            'theta_0_min_deg': 1,
            'theta_0_max_deg': 15,
            'fi_count_min': 100,
            'fi_count_max': 10000,
            'theta_count_min': 100,
            'theta_count_max': 10000,
            'l_main_min': 0,
            'l_main_max': 100,
            'l_side_min': 0,
            'l_side_max': 100,
        }

    def __init__(self):
        self.fi_s = np.radians(PhasePattern.DEFAULT_OPTIONS['fi_s_deg'])
        self.theta_s = np.radians(PhasePattern.DEFAULT_OPTIONS['theta_s_deg'])
        self.fi_0 = np.radians(PhasePattern.DEFAULT_OPTIONS['fi_0_deg'])
        self.theta_0 = np.radians(PhasePattern.DEFAULT_OPTIONS['theta_0_deg'])
        self.fi_count = PhasePattern.DEFAULT_OPTIONS['fi_count']
        self.theta_count = PhasePattern.DEFAULT_OPTIONS['theta_count']

        self.l_main = PhasePattern.DEFAULT_OPTIONS['l_main']
        self.l_side = PhasePattern.DEFAULT_OPTIONS['l_side']

        self.fi_min = np.radians(PhasePattern.DEFAULT_OPTIONS['fi_min_deg'])
        self.fi_max = np.radians(PhasePattern.DEFAULT_OPTIONS['fi_max_deg'])
        self.theta_min = np.radians(PhasePattern.DEFAULT_OPTIONS['theta_min_deg'])
        self.theta_max = np.radians(PhasePattern.DEFAULT_OPTIONS['theta_max_deg'])

        self.fi_array = None
        self.theta_array = None
        self.fi_grid = None
        self.theta_grid = None

        self.DNA = None
        self.cartesian = None

        self.results = None
        self.calc()

    def refresh(self, options):
        fi_s = np.radians(options['fi_s_deg'])
        theta_s = np.radians(options['theta_s_deg'])
        fi_0 = np.radians(options['fi_0_deg'])
        theta_0 = np.radians(options['theta_0_deg'])
        fi_count = options['fi_count']
        theta_count = options['theta_count']
        l_main = options['l_main']
        l_side = options['l_side']
        is_new_options = self._is_new_options(fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side)
        self._update_options(fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side)
        if is_new_options:
            self.calc()
        return is_new_options

    def calc(self):
        self._fill_angle_arrays()
        self.calc_DNA()
        self.calc_cartesian()
        self._save_results()

    def _save_results(self):
        self.results = {'fi_s': self.fi_s,
                        'theta_s': self.theta_s,
                        'limits_deg': self.limits_to_degrees(),
                        'fi_0': self.fi_0,
                        'theta_0': self.theta_0,
                        'fi_array': self.fi_array,
                        'theta_array': self.theta_array,
                        'DNA': self.DNA[:, :],
                        'cartesian': {'x': self.cartesian['x'],
                                      'y': self.cartesian['y'],
                                      'z': self.cartesian['z'],
                                      'tri': self.cartesian['tri']}
                        }

    def _is_new_options(self, fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side):
        return (fi_s != self.fi_s) or (theta_s != self.theta_s) or (fi_0 != self.fi_0) or (theta_0 != self.theta_0) or \
               (fi_count != self.fi_count) or (theta_count != self.theta_count) or \
               (l_main != self.l_main) or (l_side != self.l_side)

    def _update_options(self, fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side):
        self.fi_s = fi_s
        self.theta_s = theta_s
        self.fi_0 = fi_0
        self.theta_0 = theta_0
        self.fi_count = fi_count
        self.theta_count = theta_count
        self.l_main = l_main
        self.l_side = l_side

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
        self.fi_grid = self.fi_grid.T
        self.theta_grid = self.theta_grid.T
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
        tri = matplotlib.tri.Triangulation(fi, theta)
        self.cartesian = {'x': x, 'y': y, 'z': z, 'tri': tri}

    def limits_to_degrees(self):
        return np.degrees(self.fi_min), np.degrees(self.fi_max), np.degrees(self.theta_min), np.degrees(self.theta_max)

    def get_slices(self, fi_deg, theta_deg):
        fi, theta = np.radians(fi_deg), np.radians(theta_deg)
        delta_fi = self.results['fi_array'][1] - self.results['fi_array'][0]
        delta_theta = self.results['theta_array'][1] - self.results['theta_array'][0]
        index_fi = int((fi - self.fi_min) // delta_fi)
        index_theta = int((theta - self.theta_min) // delta_theta)
        return self.results['DNA'][:, index_theta], self.results['DNA'][index_fi, :]
