import numpy as np
import pytest
from PyQt5 import QtCore

from interface import MainWindow


@pytest.fixture
def widget(qtbot):
    widget_ = MainWindow()
    widget_.show()
    qtbot.addWidget(widget_)
    qtbot.mouseClick(widget_.settings_widget.btn_calc, QtCore.Qt.LeftButton)
    qtbot.waitUntil(lambda: widget_.settings_widget.isEnabled())
    return widget_


def test_line_fi_count(widget):
    assert len(widget.phase_pattern_slices_widget.line_fi.xData) == int(widget.settings_widget.fi_count.value())


def test_line_theta_count(widget):
    assert len(widget.phase_pattern_slices_widget.line_theta.xData) == int(widget.settings_widget.theta_count.value())


def test_2d_image_shape(widget):
    assert widget.phase_pattern_2d_widget.img.image.shape == (int(widget.settings_widget.fi_count.value()),
                                                              int(widget.settings_widget.theta_count.value()))


def test_2d_image(widget):
    assert np.array_equal(widget.phase_pattern_2d_widget.img.image, widget.phase_pattern.DNA)

