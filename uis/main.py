# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue May  9 21:48:46 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_object(object):
    def setupUi(self, object):
        object.setObjectName(_fromUtf8("object"))
        object.resize(395, 405)
        self.label = QtGui.QLabel(object)
        self.label.setGeometry(QtCore.QRect(70, 50, 281, 112))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayoutWidget = QtGui.QWidget(object)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 180, 289, 229))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.trainButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.trainButton.setFont(font)
        self.trainButton.setObjectName(_fromUtf8("trainButton"))
        self.horizontalLayout.addWidget(self.trainButton)
        self.runButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.runButton.setFont(font)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.horizontalLayout.addWidget(self.runButton)

        self.retranslateUi(object)
        QtCore.QMetaObject.connectSlotsByName(object)

    def retranslateUi(self, object):
        object.setWindowTitle(_translate("object", "网络故作检测系统", None))
        self.label.setText(_translate("object", "网络故障检测系统", None))
        self.trainButton.setText(_translate("object", "训练", None))
        self.runButton.setText(_translate("object", "运行", None))

