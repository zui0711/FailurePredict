import sys
from PyQt4 import QtGui, QtCore, uic
import time
import sys

qtCreatorFile_train = "uis/train_layout.ui"
qtCreatorFile_param = "uis/param_layout.ui"
qtCreatorFile_prepro = "uis/prepro_layout.ui"

Ui_trainWindow, QttrainClass = uic.loadUiType(qtCreatorFile_train)
Ui_paramWindow, QtparamClass = uic.loadUiType(qtCreatorFile_param)
Ui_preproWindow, QtpreproClass = uic.loadUiType(qtCreatorFile_prepro)


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

        self.set_param = SetParamUi()
        self.prepro = PreproUi()

    def _load_data(self):
        print("Load...")
        print self.lineEdit.text().toUtf8()

    def _set_param(self):
        print("set params...")
        self.set_param.show()

    def _prepro(self):
        self.prepro.show()

    def _detect(self):
        print("Detect...")

    def _predict(self):
        print('Predict...')


class SetParamUi(QtGui.QMainWindow, Ui_paramWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_paramWindow.__init__(self)
        self.setupUi(self)
        # self.plainTextEdit.setPlainText("abc")
        self.pushButton.clicked.connect(self.save_param)

        self.param_path = "params.py"
        # print(open(self.param_path).read())
        self.plainTextEdit.setPlainText(open(self.param_path).read())

    def save_param(self):
        s = self.plainTextEdit.toPlainText()
        fp = open(self.param_path, mode='w')
        fp.write(s)
        fp.close()


class PreproUi(QtGui.QMainWindow, Ui_preproWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_preproWindow.__init__(self)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.start)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

        # self.start2()

    def start(self):
        self.textBrowser.append("Failue detection preprocess...")
        self.wait("detection")
        self.textBrowser.append("Failue prediction preprocess...")
        self.wait("preditcion")

    # def start2(self):
    #     self.det_prepro()
    #     self.pred_prepro()

    # def det_prepro(self):
    #     print("detection preprocess")
    #     self.textBrowser.setText("Failue detection preprocess...")
    #     self.wait()
    #     self.textBrowser.append("Failue detection preprocess FINISH")
    #
    # def pred_prepro(self):
    #     print("prediction preprocess")
    #     self.textBrowser.append("Failue prediction preprocess...")
    #     self.wait()
    #     self.textBrowser.append("Failue prediction preprocess FINISH")

    def wait(self, mode):
        self.bwThread = BigWorkThread(mode)
        self.bwThread.finishSignal.connect(self.BigWorkEnd)
        self.bwThread.start()

    def BigWorkEnd(self, mode):
        if mode[0] == "detection":
            self.textBrowser.append("\nFailue detection preprocess FINISH")
        else:
            self.textBrowser.append("\nFailue prediction preprocess FINISH")


# class PreproUi(QtGui.QMainWindow, Ui_preproWindow):
#     def __int__(self):
#         QtGui.QMainWindow.__init__(self)
#         Ui_preproWindow.__init__(self)
#         self.setupUi(self)


class BigWorkThread(QtCore.QThread):
    """docstring for BigWorkThread"""
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, mode, parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.mode = mode

    def run(self):
        time.sleep(5)
        if self.mode == "detection":
            print "\nSTDOUT Failue detection preprocess..."
            self.finishSignal.emit(["detection"])
        else:
            print "\nSTDOUT Failue prediction preprocess..."
            self.finishSignal.emit(["prediction"])

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = train()
    window.show()
    sys.exit(app.exec_())

