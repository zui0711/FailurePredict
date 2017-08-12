import sys
from PyQt4 import QtGui, QtCore, uic
from interact import *


qtCreatorFile_run = "uis/run_layout.ui"
qtCreatorFile_detect = "uis/detect_layout.ui"
qtCreatorFile_predict = "uis/predict_layout.ui"


Ui_runWindow, QtrunClass = uic.loadUiType(qtCreatorFile_run)
Ui_detectWindow, QtdetectClass = uic.loadUiType(qtCreatorFile_detect)
Ui_predictWindow, QtpredictClass = uic.loadUiType(qtCreatorFile_predict)


class run(QtGui.QMainWindow, Ui_runWindow):
    def __init__(self, path, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_runWindow.__init__(self)
        self.setupUi(self)
        self.path = path
        self.lineEdit.setText(path)
        self.detectButton.clicked.connect(self._detect)
        self.predictButton.clicked.connect(self._predict)
        # self.checkBox.stateChanged.connect(self.state_changed)

    def _detect(self):
        print("Detect...")
        if self.checkBox.isChecked():
            detect = DetectUi(self.path, 2)
        else:
            detect = DetectUi(self.path, 1)
        detect.exec_()

    def _predict(self):
        print('Predict...')
        predict = PredictUi(self.path)
        predict.exec_()


class DetectUi(QtGui.QDialog, Ui_detectWindow):
    def __init__(self, path, mode):
        QtGui.QDialog.__init__(self)
        Ui_detectWindow.__init__(self)
        self.setupUi(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        self.bwThread = BackWorkThread(path, "_".join(["run_detect", str(mode)]))
        self.bwThread.start()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        # self.textBrowser.append(text)
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()


class PredictUi(QtGui.QDialog, Ui_predictWindow):
    def __init__(self, path):
        QtGui.QDialog.__init__(self)
        Ui_predictWindow.__init__(self)
        self.setupUi(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        self.bwThread = BackWorkThread(path, "run_predict")
        self.bwThread.start()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        # self.textBrowser.append(text)
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = run()
    window.show()
    sys.exit(app.exec_())