#!/usr/bin/python
"""
Evolution game, as described in The blind watchmaker by Richard Dawkins


"""

import sys, os,  queue,  math, random, threading
from PyQt5 import QtCore, Qt, QtWidgets,  QtGui
from MainWindow import Ui_MainWindow
from Flame import Flame

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

    def event(self, event):
        if event.type()== QtCore.QEvent.User:
            print('got a user event')
            self.evolution.userEvent()
            return False
        return  super().event(event)
        
    def keyPressEvent(self,e):
        print('key pressed')

    def setController(self, evolution):
        self.evolution=evolution
        evolution.setPlaceHolders(self.pics)
    
    def closeEvent(self, event):
        print('got a closing')
        self.evolution.finish()
        self.deleteLater()

class EvoThread(threading.Thread):
    """
    """
    def __init__(self, flame, width,  height, evolution):
        threading.Thread.__init__(self)
        self.flame=flame
        self.width=width
        self.height=height
        self.evolution=evolution
        
    def run(self):
        self.flame.calculate(self.width, self.height)
        self.evolution.updateFlames(self.flame)

class Evolution():
    """the controller over the development"""
    
    MaxPopulation = 16
    
    def __init__(self):
        self.queue=queue.Queue()
        self.immediate=True
        self.population=[]
        
    def setPlaceHolders(self, ph):
        self.placeHolders=ph
        self.flames=[None for p in ph]
        pass
        
    def finish(self):
        print('should save data')
        
    def start(self, dataDir):
        print('starting evolution')
        self.immediate=True
        self.dataDir=dataDir
        if not os.path.isdir(dataDir):
            print('creating directory %s', dataDir)
            os.mkdir(dataDir)
        for f in os.listdir(dataDir):
            print('got file %s'% f)
            file, ext=os.path.splitext(f)
            if ext =='.json':
                f=os.path.join(dataDir, f)
                flame=Flame()
                flame.read(f)
                flame.fileName=f
                self.population.append(flame)
        while len(self.population) < self.MaxPopulation:
            flame = Flame()
            flame.mutate()
            self.population.append(flame)
        self.inCalculation={}
        while len(self.inCalculation)<9:
            flame=random.choice(self.population)
            self.inCalculation[flame]=1
        sz=self.placeHolders[0].size()
        w=sz.width()
        h=sz.height()
        for flame in self.inCalculation.keys():
            t=EvoThread(flame, w, h, self)
            t.start()
            
    def updateFlames(self, flame):
        self.queue.put(flame)
        if self.immediate:
            qe=QtCore.QEvent(QtCore.QEvent.User)
            app.postEvent(window, qe)
    
    def createPixmap(self, flame):
        buckets=flame.buckets
        maxd=flame.maxd
        print('maxd %f'% maxd)
        #pprint(buckets) 
        w=len(buckets)
        h=len(buckets[1])
        pix=QtGui.QPixmap(w, h)
        pix.fill(QtCore.Qt.black)
        pt=QtGui.QPainter(pix)
        for i in range(w):
            for j in range(h):
                c=buckets[i][j]
                r=math.floor(255*c[0]/maxd)
                g=math.floor(255*c[1]/maxd)
                b=math.floor(255*c[2]/maxd)
                if r+g+b >0:
                    col=QtGui.QColor(r, g, b)
                    pt.setPen(col)
                    pt.drawPoint(i, j)
        pt.end()
        flame.pixmap=pix
        flame.buckets = None

    def fillPlace(self, i, flame):
        self.flames[i]=flame
        if flame.pixmap == None:
            self.createPixmap(flame)
        pix=self.placeHolders[i]
        pix.setPixmap(flame.pixmap)
        pix.update()


    def userEvent(self):
        print('process user event')
        self.immediate=False
        for i in range(len(self.flames)):
            if self.flames[i] == None:
                print('have to update a label')
                try:
                    flame=self.queue.get(False)
                    self.inCalculation.pop(flame)
                    self.fillPlace(i, flame)
                except:
                    print('no more flames to display')
                    self.immediate=True
        
app = None
window = None

def main():
    print('running evolution')
    global app
    global window
    app=Qt.QApplication(sys.argv)
    app.setApplicationName('Evolution')
    window = MainWindow()
    evolution=Evolution()
    window.setController(evolution)
    evolution.start('data')
    sys.exit(app.exec())

if __name__ == '__main__':
    """ standard convention """
    main()
