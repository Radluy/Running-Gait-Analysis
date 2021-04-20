import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qdarkstyle
import controller
from metric_description import description, corresponding_keypoints
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import time


qtCreatorFile = "src/run_analysis.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
SIDE_FILE_STRUCT = None
BACK_FILE_STRUCT = None


class popup(QtWidgets.QWidget):
    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Notification")
        self.layout = QtWidgets.QGridLayout()
        self.label = QtWidgets.QLabel(text)
        self.label.setFont(QtGui.QFont('Arial', 18))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class SideView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SideView, self).__init__(parent)
        self.video_url = None
        self.setAcceptDrops(True)
        self.layout = QtWidgets.QHBoxLayout()
        self.sideViewLabel = QtWidgets.QLabel()
        self.sideViewLabel.move(5, 10)
        self.setGeometry(5, 10, 640, 360)

        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.sideViewLabel)
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setPlaybackRate(0.5)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.stack.addWidget(self.videoWidget)

        self.set_placeholder()

    def paintEvent(self, event):
        """painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.red)
        
        painter.drawLine(500,500,200,200)"""

    def set_placeholder(self):
        pixmap = QtGui.QPixmap('./src/images/dark-placeholder.png')
        self.sideViewLabel.setPixmap(pixmap)

    def uploadVideo(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.video_url, _ = opener.getOpenFileName(self,
                                                   "Open video", QtCore.QDir.homePath())

    def uploadData(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.Directory)
        self.video_url = str(
            opener.getExistingDirectory(self, "Select Directory"))
        
    def play_video(self):
        global SIDE_FILE_STRUCT
        if SIDE_FILE_STRUCT is None:
            return
        self.mediaPlayer.setMedia(QMediaContent(
            QtCore.QUrl.fromLocalFile(SIDE_FILE_STRUCT.video)))
        self.stack.setCurrentIndex(1)
        self.mediaPlayer.play()

    def cleanAfterVideo(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.stack.setCurrentIndex(0)


class BackView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(BackView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.layout = QtWidgets.QHBoxLayout()
        self.backViewLabel = QtWidgets.QLabel()
        self.backViewLabel.move(655, 10)
        self.setGeometry(655, 10, 640, 360)

        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.backViewLabel)
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setPlaybackRate(0.5)
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.stack.addWidget(self.videoWidget)

        self.setLayout(self.layout)
        self.set_placeholder()

    def set_placeholder(self):
        pixmap = QtGui.QPixmap('./src/images/dark-placeholder.png')
        self.backViewLabel.setPixmap(pixmap)

    def uploadVideo(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.video_url, _ = opener.getOpenFileName(self,
                                                   "Open video", QtCore.QDir.homePath())

    def uploadData(self, event):
        opener = QtWidgets.QFileDialog()
        opener.setFileMode(QtWidgets.QFileDialog.Directory)
        self.video_url = str(
            opener.getExistingDirectory(self, "Select Directory"))

    def play_video(self):
        global BACK_FILE_STRUCT
        if BACK_FILE_STRUCT is None:
            return
        self.mediaPlayer.setMedia(QMediaContent(
            QtCore.QUrl.fromLocalFile(BACK_FILE_STRUCT.video)))
        self.stack.setCurrentIndex(1)
        self.mediaPlayer.play()

    def cleanAfterVideo(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.stack.setCurrentIndex(0)


class AppWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def setSideSliderLength(self):
        global SIDE_FILE_STRUCT
        try:
            self.sideViewSlider.setMaximum(len(SIDE_FILE_STRUCT.images))
        except:
            self.sideViewSlider.setMaximum(0)
        self.sideViewSlider.setValue(0)

    def setSideViewImage(self):
        global SIDE_FILE_STRUCT
        try:
            pixmap = QtGui.QPixmap(
                SIDE_FILE_STRUCT.images[self.sideViewSlider.value()])
        except:
            return
        pixmap = pixmap.scaled(640, 360)
        self.sideView.sideViewLabel.setPixmap(pixmap)
        frame_id = SIDE_FILE_STRUCT.data[self.sideViewSlider.value()]["ID"]
        self.sideLabel.setText("SIDE VIEW - FRAME: {}".format(frame_id))

        if self.syncOffset != None:
            self.backViewSlider.setValue(self.sideViewSlider.value() - self.syncOffset)

    def setBackSliderLength(self):
        global BACK_FILE_STRUCT
        try:
            self.backViewSlider.setMaximum(len(BACK_FILE_STRUCT.images))
        except:
            self.backViewSlider.setMaximum(0)
        self.backViewSlider.setValue(0)

    def setBackViewImage(self):
        global BACK_FILE_STRUCT
        try:
            pixmap = QtGui.QPixmap(
                BACK_FILE_STRUCT.images[self.backViewSlider.value()])
        except:
            return
        pixmap = pixmap.scaled(640, 360)
        self.backView.backViewLabel.setPixmap(pixmap)
        frame_id = BACK_FILE_STRUCT.data[self.backViewSlider.value()]["ID"]
        self.backLabel.setText("BACK VIEW - FRAME: {}".format(frame_id))

        if self.syncOffset != None:
            self.sideViewSlider.setValue(self.backViewSlider.value() + self.syncOffset)

    def loadData(self):
        global SIDE_FILE_STRUCT
        global BACK_FILE_STRUCT
        if self.sideView.video_url is None:
            self.raisePopup("Side View required!")
            return

        #self.raisePopup("Processing a video may take up to a few minutes!\nIn the meantime, go make yourself a cup of coffee :)")
        #time.sleep(3)
        SIDE_FILE_STRUCT = controller.backend_setup(self.sideView.video_url)
        
        if SIDE_FILE_STRUCT is None:
            self.raisePopup("Incorrect file or folder!")
            self.sideView.set_placeholder()
            self.sideLabel.setText("SIDE VIEW - FRAME: ")
            return

        try:
            BACK_FILE_STRUCT = controller.backend_setup(
                self.backView.video_url)
        except:
            SIDE_FILE_STRUCT.metric_values = controller.evaluate(
                SIDE_FILE_STRUCT.data, None)
            return
        SIDE_FILE_STRUCT.metric_values = controller.evaluate(
            SIDE_FILE_STRUCT.data, BACK_FILE_STRUCT.data)

    def hideRadioButtons(self):
        items = (self.radioLayout.itemAt(i).widget()
                 for i in range(self.radioLayout.count()))
        for radioButton in items:
            radioButton.setAutoExclusive(False)
            radioButton.setChecked(False)
            radioButton.hide()

    def chosenMetric(self):
        global SIDE_FILE_STRUCT
        global BACK_FILE_STRUCT

        if SIDE_FILE_STRUCT is None:
            return

        self.metricDescriptionText.setText("")
        chosen_metric = self.metricSelectComboBox.currentText()

        if chosen_metric == "None":
            self.hideRadioButtons()
            return
        
        self.hideRadioButtons()

        try:
            vals = SIDE_FILE_STRUCT.metric_values[chosen_metric]
        except:
            self.metricDescriptionText.setText(
                "Back view needed for this metric!")
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

        curr_metric = self.metricSelectComboBox.currentText()
        self.metricDescriptionText.setText(description[curr_metric])

    def cleanText(self):
        self.metricDescriptionText.setText("")

    def writeDescription(self, radioButton):
        items = (self.radioLayout.itemAt(i).widget()
                 for i in range(self.radioLayout.count()))
        for radioButton in items:
            if radioButton.isChecked():
                ID = radioButton.text()[7:]
        global SIDE_FILE_STRUCT
        curr_metric = self.metricSelectComboBox.currentText()
        try:
            full_angle = SIDE_FILE_STRUCT.metric_values[curr_metric][int(ID)]
            angle = round(full_angle, 2)
        except:
            return
        self.metricDescriptionText.setText("{descrip}\n\nAngle = {angle}".format(
            angle=angle, descrip=description[curr_metric]))
        chosen = self.metricSelectComboBox.currentText()
        if chosen == "Pelvic Drop" or chosen == "Parallel Legs":
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

    def raisePopup(self, text):
        self.popup = popup(text)
        desktopRect = QtWidgets.QApplication.desktop().availableGeometry()
        center = desktopRect.center()
        popup_geo = self.popup.frameGeometry()
        self.popup.setGeometry(QtCore.QRect(center.x(), center.y(), 200, 100))
        #self.popup.move(center.x() - popup_geo.width() * 0.5, center.y() - popup_geo.height() * 0.5)
        self.popup.show()

    def synchronizeViews(self, button):
        if not SIDE_FILE_STRUCT or not BACK_FILE_STRUCT:
            button.setChecked(False)
            return self.raisePopup("Both views needed for synchronization")

        if button.isChecked() == True:
            self.autoSyncCheckBox.setChecked(False)
            sideId = self.sideViewSlider.value()
            backId = self.backViewSlider.value()
            self.syncOffset = sideId - backId
        else:
            self.syncOffset = None

    def autoSync(self, button):
        if SIDE_FILE_STRUCT is None or BACK_FILE_STRUCT is None:
            button.setChecked(False)
            return self.raisePopup("Both views needed for synchronization")
        
        if button.isChecked() == True:
            self.syncCheckBox.setChecked(False)
            id_dict = controller.auto_sync(SIDE_FILE_STRUCT.data, BACK_FILE_STRUCT.data)
            self.syncOffset = id_dict["side"] - id_dict["back"]
            self.sideViewSlider.setValue(id_dict["side"])
            self.backViewSlider.setValue(id_dict["back"])
        else:
            self.syncOffset = None   

    def highlight_metric(self, metric):
        if metric in ["Pelvic Drop", "Parallel Legs"]:
            pixmap = self.backView.backViewLabel.pixmap()
        else:
            pixmap = self.sideView.sideViewLabel.pixmap()
        #painter setup
        painter = QtGui.QPainter(pixmap)
        pen = QtGui.QPen()
        pen.setWidth(6)
        pen.setColor(QtGui.QColor(255, 255, 255, 180))
        painter.setPen(pen)

        #get frame id from radiobox text
        items = (self.radioLayout.itemAt(i).widget()
                 for i in range(self.radioLayout.count()))
        for radioButton in items:
            if radioButton.isChecked():
                frame_id = radioButton.text()[7:]
                break

        points = controller.setup_highlight(frame_id, SIDE_FILE_STRUCT, BACK_FILE_STRUCT, metric)

        painter.drawLine(points[0].x, points[0].y, points[1].x, points[1].y)

        if len(points) == 3:
            painter.drawLine(points[1].x, points[1].y, points[2].x, points[2].y)

        if len(points) == 4:
            painter.drawLine(points[2].x, points[2].y, points[3].x, points[3].y)
        
        painter.end()

    def drawTrajectory(self):
        if SIDE_FILE_STRUCT is None:
            self.raisePopup("Import your video first!")
            return
        keypoint = self.trajectoryPicker.currentText()
        if keypoint == "None":
            self.hide_trajectory()
            self.sideViewTrajectory.setPixmap(QtGui.QPixmap())
            return
        
        self.sideViewTrajectory.setStyleSheet("QLabel{ background-color: transparent;}")
        trajectory = QtGui.QPixmap(SIDE_FILE_STRUCT.trajectories[keypoint])
        self.sideViewTrajectory.move(5, 18)
        self.sideViewTrajectory.setPixmap(trajectory)
        self.sideViewTrajectory.raise_()

    def hide_trajectory(self):
        self.trajectoryPicker.setCurrentIndex(0)
        self.sideViewTrajectory.lower()

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
        self.syncOffset = None
        self.sideVideoUploadButton.setIcon(
            QtGui.QIcon('src/images/video_upload2.png'))
        self.sideDataUploadButton.setIcon(
            QtGui.QIcon('src/images/folder_upload.png'))
        self.backVideoUploadButton.setIcon(
            QtGui.QIcon('src/images/video_upload2.png'))
        self.backDataUploadButton.setIcon(
            QtGui.QIcon('src/images/folder_upload.png'))
        self.playSideVideoButton.setIcon(
            QtGui.QIcon('src/images/play-button.png'))
        self.playBackVideoButton.setIcon(
            QtGui.QIcon('src/images/play-button.png'))
        self.setSignals()

    def setSignals(self):
        self.processButton.clicked.connect(self.loadData)
        self.processButton.clicked.connect(self.setSideSliderLength)
        self.processButton.clicked.connect(self.hideRadioButtons)
        self.processButton.clicked.connect(self.hide_trajectory)
        self.processButton.clicked.connect(self.cleanText)
        self.processButton.clicked.connect(self.sideView.set_placeholder)
        self.processButton.clicked.connect(self.backView.set_placeholder)
        self.sideViewSlider.valueChanged.connect(self.setSideViewImage)
        self.processButton.clicked.connect(self.setBackSliderLength)
        self.backViewSlider.valueChanged.connect(self.setBackViewImage)
        self.metricSelectComboBox.activated.connect(self.chosenMetric)
        items = (self.radioLayout.itemAt(i).widget()
                 for i in range(self.radioLayout.count()))
        for radioButton in items:
            radioButton.clicked.connect(self.writeDescription)
            radioButton.clicked.connect(lambda:self.highlight_metric(self.metricSelectComboBox.currentText()))
            policy = QtWidgets.QSizePolicy()
            policy.setRetainSizeWhenHidden(True)
            radioButton.setSizePolicy(policy)
        self.sideVideoUploadButton.clicked.connect(self.sideView.uploadVideo)
        self.sideDataUploadButton.clicked.connect(self.sideView.uploadData)
        self.backVideoUploadButton.clicked.connect(self.backView.uploadVideo)
        self.backDataUploadButton.clicked.connect(self.backView.uploadData)
        self.trajectoryPicker.currentTextChanged.connect(
            self.drawTrajectory)
        self.playBackVideoButton.clicked.connect(self.backView.play_video)
        self.backView.mediaPlayer.mediaStatusChanged.connect(
            self.backView.cleanAfterVideo)
        self.playSideVideoButton.clicked.connect(self.hide_trajectory)
        self.playSideVideoButton.clicked.connect(self.sideView.play_video)
        self.sideView.mediaPlayer.mediaStatusChanged.connect(
            self.sideView.cleanAfterVideo)
        self.syncCheckBox.stateChanged.connect(lambda:self.synchronizeViews(self.syncCheckBox))
        self.autoSyncCheckBox.stateChanged.connect(lambda:self.autoSync(self.autoSyncCheckBox))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
