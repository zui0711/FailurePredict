import sys
from PyQt4 import QtGui, uic

from do_seq2seq import *

qtCreatorFile_main = "uis/main.ui"
qtCreatorFile_l1 = "uis/l1.ui"
qtCreatorFile_l2 = "uis/l2.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile_main)
Ui_l1Window, Qtl1Class = uic.loadUiType(qtCreatorFile_l1)
Ui_l2Window, Qtl2Class = uic.loadUiType(qtCreatorFile_l2)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.l1 = l1()
        self.trainButton.clicked.connect(self.print_t)
        self.runButton.clicked.connect(self.print_r)

    def print_t(self):
        print("Train...")
        self.l1.show()

    def print_r(self):
        print("Run...")


class l1(QtGui.QMainWindow, Ui_l1Window):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_l1Window.__init__(self)
        self.setupUi(self)
        self.loadButton.clicked.connect(self.load_data)
        self.pushButton.clicked.connect(self.print_)
        self.l2 = l2()

    def load_data(self):
        print("Load...")
        print self.lineEdit.text().toUtf8()

    def print_(self):
        self.l2.show()
        print("Print...")
        tf.app.run()


class l2(QtGui.QMainWindow, Ui_l2Window):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_l2Window.__init__(self)
        self.setupUi(self)
        self.textBrowser.setText("asdf")
        self.textBrowser.append("asdfas")
        self.print_()

    def print_(self):
        for _ in xrange(100):
            self.textBrowser.append(str(_))





if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())