from mayavi import mlab
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor


class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene), show_label=False), resizable=True)


class PhasePattern3dWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.vbox = QtGui.QVBoxLayout()
        self.visualization = Visualization()
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        self.vbox.addWidget(self.ui)
        self.setLayout(self.vbox)

    def plot(self, results, log_scale):
        x = results['cartesian']['x']
        y = results['cartesian']['y']
        z = results['cartesian']['z']
        triangles = results['cartesian']['tri'].triangles
        mlab.clf()
        mlab.triangular_mesh(x, y, z, triangles)
        mlab.axes()
