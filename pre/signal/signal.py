from PyQt5 import QtGui as QG
from PyQt5 import QtCore as QC
from PyQt5 import QtWidgets

class SenderObject(QC.QObject):
    something_happened = QC.pyqtSignal()

class SnapROIItem(QtWidgets.QGraphicsItem):
    def __init__(self, parent = None):
        super(SnapROIItem, self).__init__(parent)
        self.sender = SenderObject()
    def do_something_and_emit(self):
        self.sender.something_happened.emit()

class ROIManager(QC.QObject):
    def __init__(self, parent=None):
        super(ROIManager,self).__init__(parent)
    def add_snaproi(self, snaproi):
        snaproi.sender.something_happened.connect(self.new_roi)
    def new_roi(self):
        print('Something happened in ROI!')

if __name__=="__main__":
    roimanager = ROIManager()
    snaproi = SnapROIItem()
    roimanager.add_snaproi(snaproi)
    snaproi.do_something_and_emit()