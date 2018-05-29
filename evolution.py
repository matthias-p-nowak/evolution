#!/usr/bin/python
import sys

from PyQt5.QtWidgets import *

from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        ag=QActionGroup(self)
        self.actionBreed.setActionGroup(ag)
        self.actionKill.setActionGroup(ag)
        #
        self.actionExit.triggered.connect(self.appExit)
        self.actionFullScreen.triggered.connect(self.fullScreen)
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


if __name__ == '__main__':
    print('running evolution')
    app=QApplication([])
    app.setApplicationName('Evolution')
    window = MainWindow()
    app.exec_()
