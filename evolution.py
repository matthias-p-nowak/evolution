#!/usr/bin/python
"""
Evolution game, as described in The blind watchmaker by Richard Dawkins


"""

import sys
from PyQt5 import QtCore, Qt, QtWidgets
from MainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    MainWindow, showing 9 pictures of current fractal flames
    """
    
    def __init__(self, *args, **kwargs):
        """
        based on MainWindow.ui generates a form, but adds the 9 picture placeholders (self.pics) in this procedure
        """
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pics = []
        for i in range(3):
            for j in range(3):
                ql= QtWidgets.QLabel(self.centralwidget)
                self.pics.append(ql)
                self.gl.addWidget(ql,i,j,1,1)
                ql.setText( '%d' % len(self.pics))
                ql.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeft)
                ql.setStyleSheet("color: yellow")
        # make the checkable menu items appear as radio buttons
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
        global app
        print('ok, done')
        app.closeAllWindows()
        app.quit()

    def fullScreen(self):
        self.showFullScreen()

    def keyPressEvent(self,e):
        print('key pressed')

    def setController(self, evolution):
        self.evolution=evolution
        evolution.setPlaceHolders(self.pics)
    
    def closeEvent(self, event):
        print('got a closing')
        self.evolution.finish()
        self.deleteLater()

class Evolution():
    """the controller over the development"""
    
    def __init__(self):
        pass
        
    def setPlaceHolders(self, ph):
        self.placeHolders=ph
        
    def finish(self):
        print('should save data')
        
    def start(self):
        print('starting evolution')
        
app = None

def main():
    print('running evolution')
    global app
    app=Qt.QApplication(sys.argv)
    app.setApplicationName('Evolution')
    window = MainWindow()
    evolution=Evolution()
    window.setController(evolution)
    evolution.start()
    sys.exit(app.exec())

if __name__ == '__main__':
    """ standard convention """
    main()
