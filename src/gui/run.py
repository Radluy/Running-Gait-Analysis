import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


qtCreatorFile = "run_analysis.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class AppWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())