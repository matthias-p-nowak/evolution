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
        self.evolution=Evolution(self)
        self.pics = {}
        for i in range(3):
            for j in range(3):
                ql= QtWidgets.QLabel(self.centralwidget)
                self.pics[ql] = None
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
        self.evolution.selection=1

    def selectKill(self):
        self.evolution.selection=2

    def appExit(self):
        global app
        print('ok, done')
        app.closeAllWindows()
        app.quit()

    def fullScreen(self):
        self.showFullScreen()

    def resizeEvent(self, event):
        print('got a resize')
        self.evolution.clearPix()

    def event(self, event):
        if event.type()== QtCore.QEvent.User:
            print('got a user event')
            self.evolution.userEvent()
            return False
        return  super().event(event)
        
    def keyPressEvent(self,e):
        print('key pressed')
    
    def closeEvent(self, event):
        print('got a closing')
        self.evolution.finish()
        self.deleteLater()
    def getPixSize(self):
        w=0
        h=0
        i=0
        for l,p in self.pics.items():
            i +=1
            sz=l.size()
            w += sz.width()
            h += sz.height()
        return [math.floor(w/i), math.floor(h/i)]
    
    def fillWith(self, queue):
        for l, flame in self.pics.items():
            if flame != None:
                continue
            flame=queue.pop()
            self.pics[l]=flame
            if flame.pixmap == None:
                self.evolution.createPixmap(flame)
            l.setPixmap(flame.pixmap)
            l.update()
        
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
    
    def __init__(self, mw):
        self.queue=queue.Queue()
        self.immediate=True
        self.population=[]
        self.mw=mw
        
        
    def finish(self):
        print('should save data')
        
    def start(self, dataDir, w, h):
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
        print('starting calculations')
        self.running={}
        while len(self.running)<9:
            flame=random.choice(self.population)
            if flame in self.running:
                continue
            self.running[flame]=True
            t=EvoThread(flame, w, h, self)
            t.start()
            
    def updateFlames(self, flame):
        self.queue.put(flame)
        if self.immediate:
            qe=QtCore.QEvent(QtCore.QEvent.User)
            app.postEvent(self.mw, qe)
    
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

    def clearPix(self):
        for flames in self.population:
            flames.pixmap = None

    def userEvent(self):
        print('process user event')
        self.immediate=False
        try:
            self.mw.fillWith(self.running)
        except:
            self.immediate=True
#        for i in range(len(self.flames)):
#            if self.flames[i] == None:
#                print('have to update a label')
#                try:
#                    flame=self.queue.get(False)
#                    self.running.pop(flame)
#                    self.fillPlace(i, flame)
#                except:
#                    print('no more flames to display')
#                    self.immediate=True
        
#app = None
#window = None

def main():
    print('running evolution')
    global app
    global window
    app=Qt.QApplication(sys.argv)
    app.setApplicationName('Evolution')
    window = MainWindow()
    window.evolution.start('data',  *window.getPixSize())
    sys.exit(app.exec())

if __name__ == '__main__':
    """ standard convention """
    main()
