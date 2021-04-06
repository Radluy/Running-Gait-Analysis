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
        frame_id = SIDE_FILE_STRUCT.data[self.sideViewSlider.value()]["ID"]
        self.sideLabel.setText("SIDE VIEW - FRAME: {}".format(frame_id))

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
        frame_id = BACK_FILE_STRUCT.data[self.backViewSlider.value()]["ID"]
        self.backLabel.setText("BACK VIEW - FRAME: {}".format(frame_id))

    def loadData(self):
        global SIDE_FILE_STRUCT
        global BACK_FILE_STRUCT
        try:
            SIDE_FILE_STRUCT = controller.backend_setup(self.sideView.video_url)
            BACK_FILE_STRUCT = controller.backend_setup(self.backView.video_url)
            SIDE_FILE_STRUCT.metric_values = controller.evaluate(SIDE_FILE_STRUCT.data, BACK_FILE_STRUCT.data)
        except:
            pass

    def hideRadioButtons(self):
        items = (self.radioLayout.itemAt(i).widget() for i in range(self.radioLayout.count())) 
        for radioButton in items:
            radioButton.hide()
    
    def chosenMetric(self):
        global SIDE_FILE_STRUCT
        global BACK_FILE_STRUCT

        if SIDE_FILE_STRUCT is None:
            return

        chosen_metric = self.metricSelectComboBox.currentText()
        # create radiobox array 
        self.hideRadioButtons()
        i = 0
        vals = SIDE_FILE_STRUCT.metric_values[chosen_metric]
        for val in vals.keys():
            try:
                radioButton = self.radioLayout.itemAt(i).widget()
            except:
                return
            radioButton.setText("Frame: {}".format(val))
            radioButton.show()
            i += 1

    def writeDescription(self, radioButton):
        items = (self.radioLayout.itemAt(i).widget() for i in range(self.radioLayout.count())) 
        for radioButton in items:
            if radioButton.isChecked():
                ID = radioButton.text()[7:]
        global SIDE_FILE_STRUCT
        angle = SIDE_FILE_STRUCT.metric_values[self.metricSelectComboBox.currentText()][int(ID)]
        self.metricDescriptionText.setText("Angle = {}".format(angle))

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
        self.metricSelectComboBox.activated.connect(self.chosenMetric)
        self.hideRadioButtons()
        items = (self.radioLayout.itemAt(i).widget() for i in range(self.radioLayout.count())) 
        for radioButton in items:
            radioButton.clicked.connect(self.writeDescription)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    #app.setStyleSheet(dark_stylesheet)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())