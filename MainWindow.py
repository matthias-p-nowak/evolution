# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(636, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: aqua;")
        self.centralwidget.setObjectName("centralwidget")
        self.gl = QtWidgets.QGridLayout(self.centralwidget)
        self.gl.setObjectName("gl")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 636, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setAcceptDrops(False)
        self.menuFile.setToolTip("")
        self.menuFile.setToolTipsVisible(True)
        self.menuFile.setObjectName("menuFile")
        self.menuEvolution = QtWidgets.QMenu(self.menubar)
        self.menuEvolution.setObjectName("menuEvolution")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setAutoFillBackground(True)
        self.statusBar.setStyleSheet("")
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionFullScreen = QtWidgets.QAction(MainWindow)
        self.actionFullScreen.setObjectName("actionFullScreen")
        self.actionBreed = QtWidgets.QAction(MainWindow)
        self.actionBreed.setCheckable(True)
        self.actionBreed.setObjectName("actionBreed")
        self.actionKill = QtWidgets.QAction(MainWindow)
        self.actionKill.setCheckable(True)
        self.actionKill.setChecked(True)
        self.actionKill.setObjectName("actionKill")
        self.menuFile.addAction(self.actionFullScreen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEvolution.addAction(self.actionBreed)
        self.menuEvolution.addAction(self.actionKill)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEvolution.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Evolution"))
        self.menuFile.setStatusTip(_translate("MainWindow", "The usual..."))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuEvolution.setTitle(_translate("MainWindow", "&Evolution"))
        self.actionExit.setText(_translate("MainWindow", "E&xit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Going home..."))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionFullScreen.setText(_translate("MainWindow", "Full&Screen"))
        self.actionFullScreen.setStatusTip(_translate("MainWindow", "show Evolution in full screen"))
        self.actionBreed.setText(_translate("MainWindow", "&Breed"))
        self.actionKill.setText(_translate("MainWindow", "&Kill"))

