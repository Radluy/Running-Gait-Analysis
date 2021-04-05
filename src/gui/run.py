import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qdarkstyle
import controller


qtCreatorFile = "src/gui/run_analysis.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
SIDE_FILE_STRUCT = None


class SideView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SideView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QtWidgets.QGridLayout()
        self.sideViewLabel = QtWidgets.QLabel()
        self.layout.addWidget(self.sideViewLabel)
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.sideViewLabel.move(5, 10)
        self.setGeometry(5, 10, 640, 360)
        pixmap = QtGui.QPixmap('./src/gui/images/image_placeholder.png')
        self.sideViewLabel.setPixmap(pixmap)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            self.video_url = event.mimeData().text()
            SIDE_FILE_STRUCT = controller.backend_setup(self.video_url, "") #DEBUG
            print("C")
        else:
            event.ignore()

class BackView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(BackView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QtWidgets.QGridLayout()
        self.backViewLabel = QtWidgets.QLabel()
        self.layout.addWidget(self.backViewLabel)
        self.setLayout(self.layout)
        self.initUI()

    def initUI(self):
        self.backViewLabel.move(655, 10)
        self.setGeometry(655, 10, 640, 360)
        pixmap = QtGui.QPixmap('./src/gui/images/image_placeholder.png')
        self.backViewLabel.setPixmap(pixmap)

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


class AppWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.video_url = None
        self.setupUi(self)
        self.sideView = SideView(self)
        self.backView = BackView(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    #app.setStyleSheet(dark_stylesheet)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())