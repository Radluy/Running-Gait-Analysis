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

    def uploadVideo(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.video_url, _ = opener.getOpenFileName(self, 
        "Open video", QtCore.QDir.homePath())
    
    def uploadData(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.Directory)
        self.video_url = str(opener.getExistingDirectory(self, "Select Directory"))
        
        


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

    def uploadVideo(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.video_url, _ = opener.getOpenFileName(self, 
        "Open video", QtCore.QDir.homePath())
    
    def uploadData(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.Directory)
        self.video_url = str(opener.getExistingDirectory(self, "Select Directory"))
    


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
        except:
            #TODO popup saying side view required
            return
        try:
            BACK_FILE_STRUCT = controller.backend_setup(self.backView.video_url)
        except:
            SIDE_FILE_STRUCT.metric_values = controller.evaluate(SIDE_FILE_STRUCT.data, None)
            return
        SIDE_FILE_STRUCT.metric_values = controller.evaluate(SIDE_FILE_STRUCT.data, BACK_FILE_STRUCT.data)

    def hideRadioButtons(self):
        items = (self.radioLayout.itemAt(i).widget() for i in range(self.radioLayout.count())) 
        for radioButton in items:
            radioButton.setChecked(False)
            radioButton.setAutoExclusive(False)
            radioButton.hide()
    
    def chosenMetric(self):
        global SIDE_FILE_STRUCT
        global BACK_FILE_STRUCT

        if SIDE_FILE_STRUCT is None:
            return

        self.metricDescriptionText.setText("")
        chosen_metric = self.metricSelectComboBox.currentText()
        self.hideRadioButtons()
        
        try:
            vals = SIDE_FILE_STRUCT.metric_values[chosen_metric]
        except:
            self.metricDescriptionText.setText("Back view needed for this metric!")
            return
        
        i = 0
        for val in vals.keys():
            try:
                radioButton = self.radioLayout.itemAt(i).widget()
            except:
                return
            radioButton.setText("Frame: {}".format(val))
            radioButton.setAutoExclusive(True)
            radioButton.show()
            i += 1

    def writeDescription(self, radioButton):
        items = (self.radioLayout.itemAt(i).widget() for i in range(self.radioLayout.count())) 
        for radioButton in items:
            if radioButton.isChecked():
                ID = radioButton.text()[7:]
        global SIDE_FILE_STRUCT
        try:
            angle = SIDE_FILE_STRUCT.metric_values[self.metricSelectComboBox.currentText()][int(ID)]
        except:
            return
        self.metricDescriptionText.setText("Angle = {}".format(angle))
        chosen = self.metricSelectComboBox.currentText()
        if chosen == "Pelvic Drop" or chosen == "": #TODO: next back metric
            i = 0
            for frame in BACK_FILE_STRUCT.data:
                if frame["ID"] == int(ID):
                    self.backViewSlider.setValue(i)
                    break
                i += 1
        else:
            i = 0
            for frame in SIDE_FILE_STRUCT.data:
                if frame["ID"] == int(ID):
                    self.sideViewSlider.setValue(i)
                    break
                i += 1

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.sideView = SideView(self)
        self.backView = BackView(self)
        self.setAcceptDrops(True)
        self.setSideSliderLength()
        self.setBackSliderLength()
        self.hideRadioButtons()
        self.setSignals()

    def setSignals(self):
        self.processButton.clicked.connect(self.loadData)
        self.processButton.clicked.connect(self.setSideSliderLength)
        self.sideViewSlider.valueChanged.connect(self.setSideViewImage)
        self.processButton.clicked.connect(self.setBackSliderLength)
        self.backViewSlider.valueChanged.connect(self.setBackViewImage)
        self.metricSelectComboBox.activated.connect(self.chosenMetric)
        items = (self.radioLayout.itemAt(i).widget() for i in range(self.radioLayout.count())) 
        for radioButton in items:
            radioButton.clicked.connect(self.writeDescription)
            policy = QtWidgets.QSizePolicy()
            policy.setRetainSizeWhenHidden(True)
            radioButton.setSizePolicy(policy)
        self.sideVideoUploadButton.clicked.connect(self.sideView.uploadVideo)
        self.sideDataUploadButton.clicked.connect(self.sideView.uploadData)
        self.backVideoUploadButton.clicked.connect(self.backView.uploadVideo)
        self.backDataUploadButton.clicked.connect(self.backView.uploadData)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())