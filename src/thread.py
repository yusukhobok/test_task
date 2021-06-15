from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal


class BackgroundThread(QtCore.QThread):
    def __init__(self, parent, operation, func, args, kwargs):
        super(QtCore.QThread, self).__init__(parent)
        self.operation = operation
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)


class Operation(QObject):
    finishSignal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent, func_cancel=None):
        QObject.__init__(self, parent)
        self.parent = parent
        self.func = None
        self.args = ()
        self.kwargs = {}
        self.isStop = False
        self.func_cancel = func_cancel
        self.backgroundThread = None

    def set_func(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.backgroundThread = BackgroundThread(self.parent, self, self.func, self.args, self.kwargs)
        self.backgroundThread.finished.connect(self.finish)

    def stop(self):
        self.isStop = True
        self.backgroundThread.quit()
        self.backgroundThread.terminate()
        if self.func_cancel is not None:
            self.func_cancel()

    def start(self):
        self.backgroundThread.start()

    def finish(self):
        self.finishSignal.emit(self.backgroundThread.result)

    def set_finish_function(self, func):
        def wrapper(*args, **kwargs):
            if not self.isStop:
                if func is not None:
                    func(*args, **kwargs)
        self.finishSignal.connect(wrapper)

