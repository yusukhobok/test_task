from PyQt5 import QtWidgets

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._parent = parent
        self.vbox = QtWidgets.QVBoxLayout()
        default_options = self._parent.phase_pattern.DEFAULT_OPTIONS
        self.fi_s_deg = self.add_float_item("Угол установки луча по азимуту (φ<sub>s</sub>), °", 
                                            default_options['fi_s_deg'], default_options['fi_s_min_deg'],
                                            default_options['fi_s_max_deg'], 3, 1)
        self.theta_s_deg = self.add_float_item("Угол установки луча по возвышению (θ<sub>s</sub>), °", 
                                               default_options['theta_s_deg'], default_options['theta_s_min_deg'],
                                               default_options['theta_s_max_deg'], 3, 1)
        self.fi_0_deg = self.add_float_item("Ширина главного лепестка по азимуту (φ<sub>0</sub>), °", 
                                            default_options['fi_0_deg'], default_options['fi_0_min_deg'],
                                            default_options['fi_0_max_deg'], 3, 1)
        self.theta_0_deg = self.add_float_item("Ширина главного лепестка по возвышению (θ<sub>0</sub>), °", 
                                               default_options['theta_0_deg'], default_options['theta_0_min_deg'],
                                               default_options['theta_0_max_deg'], 3, 1)
        self.fi_count = self.add_int_item("Размеры расчетной сетки по азимуту, шагов", 
                                          default_options['fi_count'], default_options['fi_count_min'],
                                          default_options['fi_count_max'])
        self.theta_count = self.add_int_item("Размеры расчетной сетки по возвышению, шагов", 
                                             default_options['theta_count'], default_options['theta_count_min'],
                                             default_options['theta_count_max'])
        self.log_scale = self.add_bool_item("Логарифмический масштаб", False)
        self.btn_calc = QtWidgets.QPushButton("Расчет")
        self.btn_calc.clicked.connect(self._parent.refresh)
        self.vbox.addWidget(self.btn_calc)
        self.setLayout(self.vbox)

    def add_horizontal_box(caption, edt):
        hbox = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel(caption)
        hbox.addWidget(lbl)
        hbox.addWidget(edt)
        return hbox

    def add_float_item(self, caption, default, min_value, max_value, decimals=3, single_step=None):
        if not min_value <= default <= max_value:
            default = min_value
        if single_step is None:
            single_step = 10 ** (-decimals)
        edt = QtWidgets.QDoubleSpinBox()
        edt.setDecimals(decimals)
        edt.setRange(min_value, max_value)
        edt.setSingleStep(single_step)
        edt.setValue(default)
        hbox = SettingsWidget.add_horizontal_box(caption, edt)
        self.vbox.addLayout(hbox)
        return edt

    def add_int_item(self, caption, default, min_value, max_value):
        if not min_value <= default <= max_value:
            default = min_value
        edt = QtWidgets.QSpinBox()
        edt.setRange(min_value, max_value)
        edt.setSingleStep(1)
        edt.setValue(default)
        hbox = SettingsWidget.add_horizontal_box(caption, edt)
        self.vbox.addLayout(hbox)
        return edt

    def add_bool_item(self, caption, default):
        chk = QtWidgets.QCheckBox("")
        chk.setChecked(default)
        hbox = SettingsWidget.add_horizontal_box(caption, chk)
        self.vbox.addLayout(hbox)
        return chk

    def to_dict(self):
        return {
            "fi_s_deg": self.fi_s_deg.value(),
            "theta_s_deg": self.theta_s_deg.value(),
            "fi_0_deg": self.fi_0_deg.value(),
            "theta_0_deg": self.theta_0_deg.value(),
            "fi_count": int(self.fi_count.value()),
            "theta_count": int(self.theta_count.value()),
            "log_scale": self.log_scale.isChecked(),
        }



