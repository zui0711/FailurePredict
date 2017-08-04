import sys
from PyQt4 import QtGui, QtCore, uic

from uis.train_func import *
from uis.run_func import *

# from do_seq2seq import *

qtCreatorFile_main = "uis/main.ui"

qtCreatorFile_l2 = "uis/l2.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile_main)

Ui_l2Window, Qtl2Class = uic.loadUiType(qtCreatorFile_l2)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.train = train()
        self.run = run()
        self.trainButton.clicked.connect(self.print_t)
        self.runButton.clicked.connect(self.print_r)

    def print_t(self):
        print("Train...")
        self.train.show()

    def print_r(self):
        print("Run...")
        self.run.show()



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


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        self.setFocus()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        self.connect(openFile, QtCore.SIGNAL('triggered()'), self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('OpenFile')

    def showDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                     '/home')
        fname = open(filename)
        data = fname.read()
        self.textEdit.setText(data)
        # self.textEdit

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    # window = Example()
    window.show()
    sys.exit(app.exec_())