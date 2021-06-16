import matplotlib.tri
import numpy as np


class PhasePattern:
    """Класс, в котором выполняются расчеты диаграммы направленности фазированной антенной решетки (ДНА).

    Атрибуты:
    fi_s: угол установки луча по азимуту, рад.
    theta_s: угол установки луча по возвышению, рад.
    fi_0: ширина главного лепестка по азимуту, рад.
    theta_0: ширина главного лепестка по возвышению, рад.
    fi_count: размеры расчетной сетки по азимуту.
    theta_count: размеры расчетной сетки по возвышению.
    l_main: уровень главного лепестка ДНА.
    l_side: уровень бокового лепестка ДНА.
    fi_min: минимально возможное значения азимута, рад.
    fi_max: максимально возможное значение азимута, рад.
    theta_min: минимально возможное значение возвышения, рад.
    theta_max: максимально возможное значение возвышения, рад.
    fi_array: массив всех значений азимута, рад (количество элементов равно fi_count).
    theta_array: массив всех значений возвышения, рад (количество элементов равно theta_count).
    log_scale: отображение в логарифмическом масштабе
    DNA: рассчитываемая матрица ДНА (размером fi_count на theta_count).
    cartesian: результат преобразования сферических в декартовы координаты.
    results: словарь с результатами прошлых расчетов (необходим для того, чтобы при расчете новых даннных можно было 
             работать со старыми.
    DEFAULT_OPTIONS - значения атрибутов по умолчанию
    """
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
            'fi_0_min_deg': 0.001,
            'fi_0_max_deg': 15,
            'theta_0_min_deg': 0.001,
            'theta_0_max_deg': 15,
            'fi_count_min': 100,
            'fi_count_max': 10000,
            'theta_count_min': 100,
            'theta_count_max': 10000,
            'l_main_min': 0,
            'l_main_max': 100,
            'l_side_min': 0,
            'l_side_max': 100,
            'log_scale': False
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
        self.log_scale = PhasePattern.DEFAULT_OPTIONS['log_scale']

        self.fi_array = None
        self.theta_array = None
        self._fi_grid = None
        self._theta_grid = None

        self.DNA = None
        self.cartesian = None

        self.results = None
        self._calc()

    def refresh(self, options):
        """Перерасчет параметров ДНА"""
        fi_s = np.radians(options['fi_s_deg'])
        theta_s = np.radians(options['theta_s_deg'])
        fi_0 = np.radians(options['fi_0_deg'])
        theta_0 = np.radians(options['theta_0_deg'])
        fi_count = options['fi_count']
        theta_count = options['theta_count']
        l_main = options['l_main']
        l_side = options['l_side']
        log_scale = options['log_scale']
        is_new_options = self._is_new_options(fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side,
                                              log_scale)
        self._update_options(fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side, log_scale)
        if is_new_options:
            self._calc()
        return is_new_options

    def _calc(self):
        self._fill_angle_arrays()
        self._calc_DNA()
        self._calc_cartesian()
        self._save_results()

    def _save_results(self):
        """Сохранение результатов расчета"""
        self.results = {'fi_s': self.fi_s,
                        'theta_s': self.theta_s,
                        'limits_deg': self._limits_to_degrees(),
                        'fi_0': self.fi_0,
                        'theta_0': self.theta_0,
                        'fi_array': self.fi_array,
                        'theta_array': self.theta_array,
                        'log_scale': self.log_scale,
                        'DNA': self.DNA[:, :],
                        'cartesian': {'x': self.cartesian['x'],
                                      'y': self.cartesian['y'],
                                      'z': self.cartesian['z'],
                                      'tri': self.cartesian['tri']}
                        }

    def _is_new_options(self, fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side, log_scale):
        """Проверка, изменились ли исходные данные по сравнению с прошлым расчетом"""
        return (fi_s != self.fi_s) or (theta_s != self.theta_s) or (fi_0 != self.fi_0) or (theta_0 != self.theta_0) or \
               (fi_count != self.fi_count) or (theta_count != self.theta_count) or \
               (l_main != self.l_main) or (l_side != self.l_side) or (log_scale != self.log_scale)

    def _update_options(self, fi_s, theta_s, fi_0, theta_0, fi_count, theta_count, l_main, l_side, log_scale):
        self.fi_s = fi_s
        self.theta_s = theta_s
        self.fi_0 = fi_0
        self.theta_0 = theta_0
        self.fi_count = fi_count
        self.theta_count = theta_count
        self.l_main = l_main
        self.l_side = l_side
        self.log_scale = log_scale

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

    def _calc_DNA(self):
        """расчет ДНА"""
        self._fi_grid, self._theta_grid = np.meshgrid(self.fi_array, self.theta_array)
        self._fi_grid = self._fi_grid.T
        self._theta_grid = self._theta_grid.T
        self.DNA = self._calc_G(self._fi_grid, self._theta_grid)

    def _calc_cartesian(self):
        """пересчет ДНА из сферических в декартовы координаты"""
        fi_gaps = len(self.fi_array) // 100
        if fi_gaps == 0:
            fi_gaps = 1
        theta_gaps = len(self.theta_array) // 100
        if theta_gaps == 0:
            theta_gaps = 1
        fi = self._fi_grid[::fi_gaps, ::theta_gaps].flatten()
        theta = self._theta_grid[::fi_gaps, ::theta_gaps].flatten()
        r = self.DNA[::fi_gaps, ::theta_gaps].flatten()
        if self.log_scale:
            eps = np.finfo(r.dtype).eps
            r = np.log10(r + eps)

        x = r * np.sin(theta) * np.cos(fi)
        y = r * np.sin(theta) * np.sin(fi)
        z = r * np.cos(theta)
        tri = matplotlib.tri.Triangulation(fi, theta)
        self.cartesian = {'x': x, 'y': y, 'z': z, 'tri': tri}

    def _limits_to_degrees(self):
        """возвращает размеры модели в градусах"""
        return np.degrees(self.fi_min), np.degrees(self.fi_max), np.degrees(self.theta_min), np.degrees(self.theta_max)

    def get_slices(self, fi_deg, theta_deg):
        """возвращает срез ДНА по азимуту и срез ДНА по возвышению (задаются в градусах)"""
        fi, theta = np.radians(fi_deg), np.radians(theta_deg)
        delta_fi = self.results['fi_array'][1] - self.results['fi_array'][0]
        delta_theta = self.results['theta_array'][1] - self.results['theta_array'][0]
        index_fi = int((fi - self.fi_min) // delta_fi)
        index_theta = int((theta - self.theta_min) // delta_theta)
        slice_fi = self.results['DNA'][index_fi, :]
        slice_theta = self.results['DNA'][:, index_theta]
        return slice_theta, slice_fi
