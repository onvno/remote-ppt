import sys
import time

from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from PyQt5.QtWidgets import *


# Subclassing QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):

    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("A Increasing")
            count += 1
        

# Subclassing QObject and using moveToThread
# http://blog.qt.digia.com/blog/2007/07/05/qthreads-no-longer-abstract
class SomeObject(QObject):

    finished = pyqtSignal(int)

    def long_running(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("B Increasing")
            count += 1
        self.finished.emit(12345)

# Using a QRunnable
# http://qt-project.org/doc/latest/qthreadpool.html
# Note that a QRunnable isn't a subclass of QObject and therefore does
# not provide signals and slots.
class Runnable(QRunnable):

    def run(self):
        count = 0
        app = QCoreApplication.instance()
        while count < 5:
            print("C Increasing")
            time.sleep(1)
            count += 1
        app.quit()


def using_q_thread():
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    thread = AThread()
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())

def using_move_to_thread():
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    objThread = QThread()
    pp = 3
    def test(num):
        print("test:::", num)
        objThread.quit()
        
    
    obj = SomeObject()
    obj.moveToThread(objThread)
    obj.finished.connect(test)

    objThread.started.connect(obj.long_running)
    objThread.start()
    objThread.finished.connect(app.exit)
    
    sys.exit(app.exec_())

def using_q_runnable():
    app = QCoreApplication([])
    runnable = Runnable()
    QThreadPool.globalInstance().start(runnable)
    sys.exit(app.exec_())

if __name__ == "__main__":
    # using_q_thread()
    using_move_to_thread()