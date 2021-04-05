import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qdarkstyle
import controller


qtCreatorFile = "src/run_analysis.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
SIDE_FILE_STRUCT = None
BACK_FILE_STRUCT = None

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
        pixmap = QtGui.QPixmap('./src/images/image_placeholder.png')
        self.sideViewLabel.setPixmap(pixmap)

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
        pixmap = QtGui.QPixmap('./src/images/image_placeholder.png')
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

    def setSideSliderLength(self):
        global SIDE_FILE_STRUCT
        try:
            self.sideViewSlider.setMaximum(len(SIDE_FILE_STRUCT.images))
        except:
            self.sideViewSlider.setMaximum(0)

    def setSideViewImage(self):
        global SIDE_FILE_STRUCT
        try:
            pixmap = QtGui.QPixmap(SIDE_FILE_STRUCT.images[self.sideViewSlider.value()])
        except:
            return
        pixmap = pixmap.scaled(640, 360)
        self.sideView.sideViewLabel.setPixmap(pixmap)

    def setBackSliderLength(self):
        global BACK_FILE_STRUCT
        try:
            self.backViewSlider.setMaximum(len(BACK_FILE_STRUCT.images))
        except:
            self.backViewSlider.setMaximum(0)

    def setBackViewImage(self):
        global BACK_FILE_STRUCT
        try:
            pixmap = QtGui.QPixmap(BACK_FILE_STRUCT.images[self.backViewSlider.value()])
        except:
            return
        pixmap = pixmap.scaled(640, 360)
        self.backView.backViewLabel.setPixmap(pixmap)

    def loadData(self):
        global SIDE_FILE_STRUCT
        global BACK_FILE_STRUCT
        try:
            SIDE_FILE_STRUCT = controller.backend_setup(self.sideView.video_url)
            BACK_FILE_STRUCT = controller.backend_setup(self.backView.video_url)
        except:
            pass

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.sideView = SideView(self)
        self.backView = BackView(self)
        self.setAcceptDrops(True)
        self.processButton.clicked.connect(self.loadData)
        self.processButton.clicked.connect(self.setSideSliderLength)
        self.setSideSliderLength()
        self.sideViewSlider.valueChanged.connect(self.setSideViewImage)
        self.processButton.clicked.connect(self.setBackSliderLength)
        self.setBackSliderLength()
        self.backViewSlider.valueChanged.connect(self.setBackViewImage)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    #app.setStyleSheet(dark_stylesheet)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())