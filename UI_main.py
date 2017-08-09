import sys
from PyQt4 import QtGui, QtCore, uic

from uis.train_func import *
from uis.run_func import *

# from do_seq2seq import *

qtCreatorFile_main = "uis/main.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile_main)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.trainButton.clicked.connect(self.print_t)
        self.runButton.clicked.connect(self.print_r)

    def print_t(self):
        print("Train...")
        self.train = train()
        self.train.show()

    def print_r(self):
        print("Run...")
        self.run = run()
        self.run.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    # window = Example()
    window.show()
    sys.exit(app.exec_())