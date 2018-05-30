#!/usr/bin/python
import sys

from PyQt5 import QtCore, Qt, QtWidgets, QtGui

from MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pics=[]
        for i in range(3):
            for j in range(3):
                ql= QtWidgets.QLabel(self.centralwidget)
                self.pics.append(ql)
                self.gl.addWidget(ql,i,j,1,1)
                ql.setText( 'ah %d %d' % (i,j))
        ag=QtWidgets.QActionGroup(self)
        self.actionBreed.setActionGroup(ag)
        self.actionKill.setActionGroup(ag)
        #
        self.actionExit.triggered.connect(self.appExit)
        self.actionFullScreen.triggered.connect(self.fullScreen)
        #
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
       # last one
        self.show()

    def selectBreed(self):
        self.selection=1

    def selectKill(self):
        self.selection=2

    def appExit(self):
        print('ok, done')
        sys.exit(0)

    def fullScreen(self):
        self.showFullScreen()

    def keyPressEvent(self,e):
        print('key pressed')

if __name__ == '__main__':
    print('running evolution')
    app=Qt.QApplication([])
    app.setApplicationName('Evolution')
    window = MainWindow()
    app.exec_()
