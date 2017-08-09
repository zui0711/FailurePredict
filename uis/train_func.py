import sys
from PyQt4 import QtGui, QtCore, uic
import time
import sys

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
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_trainWindow.__init__(self)
        self.setupUi(self)
        self.loadButton.clicked.connect(self._load_data)
        self.paramButton.clicked.connect(self._set_param)
        self.preproButton.clicked.connect(self._prepro)
        self.detectButton.clicked.connect(self._detect)
        self.predictButton.clicked.connect(self._predict)


    def _load_data(self):
        print("Load...")
        print self.lineEdit.text().toUtf8()

    def _set_param(self):
        print("set params...")
        set_param = SetParamUi()
        set_param.exec_()

    def _prepro(self):
        print("prepro...")
        prepro = PreproUi()
        prepro.exec_()

    def _detect(self):
        print("Detect...")
        detect = DetectUi()
        detect.exec_()

    def _predict(self):
        print('Predict...')
        predict = PredictUi()
        predict.exec_()


class SetParamUi(QtGui.QDialog, Ui_paramWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_paramWindow.__init__(self)
        self.setupUi(self)
        self.saveButton.clicked.connect(self.save_param)

        self.param_path = "params.py"
        # print(open(self.param_path).read())
        self.plainTextEdit.setPlainText(open(self.param_path).read())

    def save_param(self):
        s = self.plainTextEdit.toPlainText()
        fp = open(self.param_path, mode='w')
        fp.write(s)
        fp.close()


class PreproUi(QtGui.QDialog, Ui_preproWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self)
        Ui_preproWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        self.textBrowser.append(text)
        # cursor = self.textBrowser.textCursor()
        # cursor.movePosition(QtGui.QTextCursor.End)
        # cursor.insertText(text)
        # self.textBrowser.setTextCursor(cursor)
        # self.textBrowser.ensureCursorVisible()


    def start(self):
        self.textBrowser.append("Failue detection preprocess...")
        self.wait("detection")
        self.textBrowser.append("Failue prediction preprocess...")
        self.wait("preditcion")
        # print "pp"

    def wait(self, mode):
        self.bwThread = BackWorkThread(mode)
        self.bwThread.finishSignal.connect(self.BackWorkEnd)
        self.bwThread.start()

    def BackWorkEnd(self, mode):
        if mode[0] == "detection":
            # self.textBrowser.append()
            print "Failue detection preprocess FINISH"
        else:
            # self.textBrowser.append()
            print "Failue prediction preprocess FINISH"


class DetectUi(QtGui.QDialog, Ui_detectWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_detectWindow.__init__(self)
        self.setupUi(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        self.textBrowser.append(text)

        self.bwThread = BackWorkThread("detect")
        self.bwThread.finishSignal.connect(self.BackWorkEnd)
        self.bwThread.start()


class PredictUi(QtGui.QDialog, Ui_predictWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_predictWindow.__init__(self)
        self.setupUi(self)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        self.textBrowser.append(text)

        self.bwThread = BackWorkThread("predict")
        self.bwThread.finishSignal.connect(self.BackWorkEnd)
        self.bwThread.start()

class BackWorkThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(str)

    def __init__(self, mode, parent=None):
        super(BackWorkThread, self).__init__(parent)
        self.mode = mode

    def run(self):
        time.sleep(6)
        if self.mode == "detection":
            print "STDOUT Failue detection preprocess..."
            self.finishSignal.emit("detection")
        else:
            print "STDOUT Failue prediction preprocess..."
            self.finishSignal.emit("prediction")



class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = train()
    window.show()
    sys.exit(app.exec_())
    # app.exec_()
