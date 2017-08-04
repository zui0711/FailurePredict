import sys
from PyQt4 import QtGui, QtCore, uic


qtCreatorFile_train = "uis/train_layout.ui"
qtCreatorFile_param = "uis/param_layout.ui"

Ui_trainWindow, QttrainClass = uic.loadUiType(qtCreatorFile_train)
Ui_paramWindow, QtparamClass = uic.loadUiType(qtCreatorFile_param)

class train(QtGui.QMainWindow, Ui_trainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_trainWindow.__init__(self)
        self.setupUi(self)
        self.loadButton.clicked.connect(self.load_data)
        self.paramButton.clicked.connect(self.set_param)
        self.preproButton.clicked.connect(self.prepro)
        self.detectButton.clicked.connect(self.detect)
        self.predictButton.clicked.connect(self.predict)

        self.set_param = set_param()

    def load_data(self):
        print("Load...")
        print self.lineEdit.text().toUtf8()

    def set_param(self):
        print("set params...")
        self.set_param.show()

    def prepro(self):
        print("Failue detection preprocess...")
        print("Failue prediction preprocess...")

    def detect(self):
        print("Detect...")

    def predict(self):
        print('Predict...')


class set_param(QtGui.QMainWindow, Ui_paramWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_paramWindow.__init__(self)
        self.setupUi(self)
        # self.plainTextEdit.setPlainText("abc")
        self.pushButton.clicked.connect(self.save_param)

        self.param_path = "params.py"
        print(open(self.param_path).read())
        self.plainTextEdit.setPlainText(open(self.param_path).read())

    def save_param(self):
        s = self.plainTextEdit.toPlainText()
        fp = open(self.param_path, mode='w')
        fp.write(s)
        fp.close()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = train()
    window.show()
    sys.exit(app.exec_())
