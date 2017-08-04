import sys
from PyQt4 import QtGui, QtCore, uic


qtCreatorFile_run = "uis/run_layout.ui"


Ui_runWindow, QtrunClass = uic.loadUiType(qtCreatorFile_run)


class run(QtGui.QMainWindow, Ui_runWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        Ui_runWindow.__init__(self)
        self.setupUi(self)
        # self.detectButton.clickedQtGui.QMainWindow, Ui_runWindow.connect()

        self.detectButton.clicked.connect(self.print_)
        self.predictButton.clicked.connect(self.print_)
        self.checkBox.stateChanged.connect(self.state_changed)

    def print_(self):
        # self.l2.show()
        print("Print...")
        # tf.app.run()

    def state_changed(self):
        if self.checkBox.isChecked():
            # self.my_label.setText("CHECKED!")
            print "1"
        else:
            # self.my_label.setText("UNCHECKED!")
            print "2"


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = run()
    window.show()
    sys.exit(app.exec_())