import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


qtCreatorFile = "run_analysis.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
    

class AppWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            self.video_url = event.mimeData().text()
        else:
            event.ignore()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.video_url = None
        self.setupUi(self)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())