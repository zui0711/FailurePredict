import sys
from PyQt4 import QtGui, QtCore, uic
import time
import sys
from interact import *
from os.path import join as pjoin

qtCreatorFile_train = "uis/train_layout.ui"
qtCreatorFile_param = "uis/param_layout.ui"
qtCreatorFile_prepro = "uis/prepro_layout.ui"
qtCreatorFile_detect = "uis/detect_layout.ui"
qtCreatorFile_predict = "uis/predict_layout.ui"

Ui_trainWindow, QttrainClass = uic.loadUiType(qtCreatorFile_train)
Ui_paramWindow, QtparamClass = uic.loadUiType(qtCreatorFile_param)
Ui_preproWindow, QtpreproClass = uic.loadUiType(qtCreatorFile_prepro)
Ui_detectWindow, QtdetectClass = uic.loadUiType(qtCreatorFile_detect)
Ui_predictWindow, QtpredictClass = uic.loadUiType(qtCreatorFile_predict)


class train(QtGui.QMainWindow, Ui_trainWindow):
    def __init__(self, path, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_trainWindow.__init__(self)
        self.setupUi(self)
        self.loadButton.clicked.connect(self._load_data)
        self.paramButton.clicked.connect(self._set_param)
        self.preproButton.clicked.connect(self._prepro)
        self.detectButton.clicked.connect(self._detect)
        self.predictButton.clicked.connect(self._predict)
        self.path = path

    def _load_data(self):
        print("Load...")
        print self.lineEdit.text().toUtf8()
        self.path = str(self.lineEdit.text().toUtf8())

    def _set_param(self):
        print("set params...")
        set_param = SetParamUi(self.path)
        set_param.exec_()

    def _prepro(self):
        print("prepro...")
        prepro = PreproUi(self.path)
        prepro.exec_()

    def _detect(self):
        print("Detect...")
        detect = DetectUi(self.path)
        detect.exec_()

    def _predict(self):
        print('Predict...')
        predict = PredictUi(self.path)
        predict.exec_()

    def get_path(self):
        return self.path


class SetParamUi(QtGui.QDialog, Ui_paramWindow):
    def __init__(self, path):
        QtGui.QDialog.__init__(self)
        Ui_paramWindow.__init__(self)
        self.setupUi(self)
        self.saveButton.clicked.connect(self.save_param)
        self.param_path = pjoin(path, "params.py")

        self.plainTextEdit.setPlainText(open("params.py").read())

    def save_param(self):
        s = self.plainTextEdit.toPlainText()
        open("params.py", mode='w').write(s)
        open(self.param_path, mode='w').write(s)


class PreproUi(QtGui.QDialog, Ui_preproWindow):
    def __init__(self, path, parent=None):
        QtGui.QDialog.__init__(self)
        Ui_preproWindow.__init__(self)
        self.setupUi(self)
        # self.path = path
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        self.bwThread = BackWorkThread(path, "train_prepro")
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


class DetectUi(QtGui.QDialog, Ui_detectWindow):
    def __init__(self, path):
        QtGui.QDialog.__init__(self)
        Ui_detectWindow.__init__(self)
        self.setupUi(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

        self.bwThread = BackWorkThread(path, "train_detect")
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

        self.bwThread = BackWorkThread(path, "train_predict")
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


# class BackWorkThread(QtCore.QThread):
#     finishSignal = QtCore.pyqtSignal(str)
#
#     def __init__(self, mode, parent=None):
#         super(BackWorkThread, self).__init__(parent)
#         self.mode = mode
#
#     def run(self):
#         time.sleep(3)
#         if self.mode == "train_prepro":
#             print "STDOUT TRAIN PREPROCESS..."
#         elif self.mode == "train_detect":
#             print "STDOUT TRAIN DETECT..."
#         elif self.mode == "train_predict":
#             print "STDOUT TRAIN PREDICT..."
#         elif self.mode == "run_detect":
#             print "STDOUT RUN DETECT..."
#         elif self.mode == "run_predict":
#             print "STDOUT RUN PREDICT..."
#         else:
#             exit(1)
#


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = train()
    window.show()
    sys.exit(app.exec_())
    # app.exec_()
