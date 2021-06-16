from PyQt5 import QtCore
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
    finish_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent, func_cancel=None):
        QObject.__init__(self, parent)
        self.parent = parent
        self.func = None
        self.args = ()
        self.kwargs = {}
        self.isStop = False
        self.func_cancel = func_cancel
        self.background_thread = None

    def set_func(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.background_thread = BackgroundThread(self.parent, self, self.func, self.args, self.kwargs)
        self.background_thread.finished.connect(self.finish)

    def stop(self):
        self.isStop = True
        self.background_thread.quit()
        self.background_thread.terminate()
        if self.func_cancel is not None:
            self.func_cancel()

    def start(self):
        self.background_thread.start()

    def finish(self):
        self.finish_signal.emit(self.background_thread.result)

    def set_finish_function(self, func, *args, **kwargs):
        def wrapper():
            if not self.isStop:
                if func is not None:
                    func(*args, **kwargs)
        self.finish_signal.connect(wrapper)
