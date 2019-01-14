# affichage
import math

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF
from PyQt5.QtWidgets import QApplication
import numpy as np


import pickle
import piste
import affichage
import mouse_tracker
import astar2
import presentationvoiture

LARGEUR = piste.LARGEUR +1
WIDTH = 900  # Initial window width (pixels)
HEIGHT = 500  # Initial window height (pixels)
AIRPORT_Z_VALUE = 0
TK_COLOR = "black"
ANIMATION_DELAY = 51  # milliseconds


class PanZoomView(QtWidgets.QGraphicsView):
    """An interactive view that supports Pan and Zoom functions"""

    def __init__(self, scene):
        super().__init__(scene)
        # enable anti-aliasing
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # enable drag and drop of the view
        self.setDragMode(self.ScrollHandDrag)

    def wheelEvent(self, event):
        """Overrides method in QGraphicsView in order to zoom it when mouse scroll occurs"""
        factor = math.pow(1.001, event.angleDelta().y())
        self.zoom_view(factor)

    @QtCore.pyqtSlot(int)
    def zoom_view(self, factor):
        """Updates the zoom factor of the view"""
        self.setTransformationAnchor(self.AnchorUnderMouse)
        super().scale(factor, factor)


class Dessin(QtWidgets.QWidget):
    def __init__(self,choice, car):
        super().__init__()

        # Settings
        self.setWindowTitle('Trajectoire')
        self.resize(WIDTH, HEIGHT)

        self.play = False
        self.re = False
        self.ready = False
        self.voiturechoisie = False

        self.car = car


        if choice == 1:
            self.chemin = piste.creationpiste(300)
            self.lancerastar()

        elif choice == 2:
            try:
                with open('data','rb') as fichier:
                    mon_depickler=pickle.Unpickler(fichier)
                    self.chemin  = mon_depickler.load()
                    self.lancerastar()
            except:
                print("Il n'y a pas de fichier enregistré")


        elif choice == 3:
            try:
                with open('alldata','rb') as fichier:
                    depickler = pickle.Unpickler(fichier)
                    [self.chemin,self.car] = depickler.load()
                    self.mainwindows()
                    self.ready = True
            except:
                print("Il n'y a pas de fichier enregistré")
        else:

            self.ex = mouse_tracker.MouseTracker()
            self.ex.listeMouseTracker.connect(self.listemousetracker)
            self.ex.setWindowModality(QtCore.Qt.ApplicationModal)
            self.ex.show()

    def defvoiture(self):

        voiture = self.firstview.choisie
        A=[voiture[0],float(voiture[1]),float(voiture[2]),int(voiture[3]),float(voiture[4]),int(voiture[5]),float(voiture[6]),float(voiture[7])]
        [self.car.name,self.car.vitessemax,accelerationmax,virage,self.car.empattement,self.car.masse, self.car.longueur, self.car.largeur] = A
        self.car.pasvirage = float(virage)*np.pi/(180*self.car.deltavirage)
        self.car.pasacceleration = float(accelerationmax)/self.car.deltaacc
        self.voiturechoisie = True
        self.ready =True

    def lancerastar(self):
        self.firstview = presentationvoiture.FirstView()
        self.firstview.voiturechoisie.connect(self.defvoiture)
        self.firstview.show()

    def mainwindows(self):
        self.piste = self.chemin[0]
        # create components
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('green'))
        self.view = PanZoomView(self.scene)
        self.time_entry = QtWidgets.QLineEdit()
        toolbar = self.create_toolbar()
        self.add_piste()



        self.moving_car = affichage.CarMotion(self, self.car)
        # invert y axis for the view


        # add components to the root_layout
        root_layout.addWidget(self.view)
        root_layout.addLayout(toolbar)
        self.show()

    def create_toolbar(self):
        # create layout for time controls and entry
        toolbar = QtWidgets.QHBoxLayout()

        def add_button(text, slot):
            """adds a button to the hbox and connects the slot"""
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(slot)
            toolbar.addWidget(button)

        # lambda function allows to pass extra arguments to slots
        # added space around '-' character to avoid different look and feel
        add_button(' - ', lambda: self.view.zoom_view(1/1.1))
        add_button('+', lambda: self.view.zoom_view(1.1))
        toolbar.addStretch()
        add_button('|>', self.playpause)
        add_button('R', self.redemarrer)
        add_button('Save Track',self.sauvegarder)
        add_button('Save Simu', self.savesimu)
        toolbar.addStretch()

        def add_shortcut(text, slot):
            """creates an application-wide key binding"""
            shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(text), self)
            shortcut.activated.connect(slot)

        add_shortcut('+', lambda: self.view.zoom_view(1.1))
        add_shortcut('-', lambda: self.view.zoom_view(1 / 1.1))
        add_shortcut(' ', self.playpause)
        add_shortcut('R', self.redemarrer)
        add_shortcut('P',self.sauvegarder)
        add_shortcut('q', QtCore.QCoreApplication.instance().quit)
        return toolbar

    def add_piste(self):

        track_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(track_group)

        pen = QPen(QtGui.QColor(TK_COLOR), LARGEUR)
        pen.setJoinStyle(Qt.RoundJoin)
        self.extrem(4)

        path = QtGui.QPainterPath()
        path.moveTo(self.piste[0].x, self.piste[0].y)
        for i in range(1, len(self.piste)):
            path.lineTo(self.piste[i].x, self.piste[i].y)
        #self.scene.addPolygon(Polygone(self.chemin[1][-1],self.chemin[2][-1],self.piste[-1],self.piste[-5], 20), QPen(QtGui.QColor(TK_COLOR), 1), QBrush(QColor(TK_COLOR)))
        item = QtWidgets.QGraphicsPathItem(path, track_group)
        item.setPen(pen)
        
            
    def extrem(self,nb):
        deltax,deltay = self.piste[nb+1].x-self.piste[0].x,self.piste[nb+1].y-self.piste[0].y
        dx,dy=self.piste[-(nb+2)].x-self.piste[-1].x,self.piste[-(nb+2)].y-self.piste[-1].y
        self.dessin(self.chemin[1][0],self.chemin[2][0],self.piste[0],self.piste[nb+1],1)
        self.dessin(self.chemin[1][-1],self.chemin[2][-1],self.piste[-1],self.piste[-(nb+2)],1)
        for i in range(1,nb):
            Pi=piste.Point(self.chemin[2][0].x+i*deltax/nb,self.chemin[2][0].y+i*deltay/nb)
            P1,P2=self.dessininter(self.chemin[1][0],self.chemin[2][0],Pi)
            self.dessin(P1,P2,self.piste[0],self.piste[nb+1],(i+1)%2)
            Pi2=piste.Point(self.chemin[2][-1].x+i*dx/nb,self.chemin[2][-1].y+i*dy/nb)
            P3,P4=self.dessininter(self.chemin[1][-1],self.chemin[2][-1],Pi2)
            self.dessin(P3,P4,self.piste[-1],self.piste[-(nb+2)],(i+1)%2)
            
    def dessininter(self,Point1,Point2,Point3):
        Deltax,Deltay=Point1.x-Point2.x,Point1.y-Point2.y
        P4=piste.Point(Point3.x+Deltax,Point3.y+Deltay)
        return(Point3,P4)
        
    def dessin(self,Point1, Point2, pointpiste1,pointpiste2,nb):
        Deltax,Deltay=(Point1.x-Point2.x),(Point1.y-Point2.y)
        deltax,deltay=pointpiste1.x-pointpiste2.x,pointpiste1.y-pointpiste2.y
        #V2=math.sqrt((Deltax)**2+(Deltay)**2)/10
        v=math.sqrt(deltax**2+deltay**2)
        V2=LARGEUR/10
        pen = QPen(QtGui.QColor('white'),V2)
        pen.setCapStyle(Qt.SquareCap)
        pen.setJoinStyle(Qt.RoundJoin)
        #self.scene.addLine(Point1.x,Point1.y,Point2.x,Point2.y,QPen(QtGui.QColor('red'),0.5))
        if v!=0:
            deltax,deltay=deltax/v,deltay/v
        if nb==1:
            for i in range(1,5):
                P1=piste.Point(Point1.x-i*Deltax/5,Point1.y-i*Deltay/5)
                P2=piste.Point(Point1.x -i*Deltax/5 + V2*deltax*0.5,Point1.y -i*Deltay/5+V2*deltay*0.5)
                self.scene.addLine(P1.x,P1.y,P2.x,P2.y,pen)
        else:
            for i in range(5):
                P1=piste.Point(Point1.x-(2*i+1)*Deltax/10,Point1.y-(2*i+1)*Deltay/10)
                P2=piste.Point(Point1.x-(2*i+1)*Deltax/10 + V2*deltax*0.5,Point1.y -(2*i+1)*Deltay/10+V2*deltay*0.5)
                self.scene.addLine(P1.x,P1.y,P2.x,P2.y,pen)

            
    @QtCore.pyqtSlot()
    def playpause(self):
        """this slot toggles the replay using the timer as model"""
        if self.play:
            self.play = False
        else:
            self.play = True
            
    def redemarrer(self):
        self.re = True

    
    def sauvegarder(self):
        with open('data','wb') as fichier:
            mon_picker=pickle.Pickler(fichier)
            mon_picker.dump(self.chemin)
        print("Sauvegarde réussie ")

    def listemousetracker(self):
        self.chemin = self.ex.chemin
        self.lancerastar()

    def miseajour(self):
        if self.voiturechoisie:
            astar2.astar(self.chemin, self.car)
            self.voiturechoisie = False
            self.mainwindows()
        if self.ready:
            self.moving_car.updateValues()

    def savesimu(self):
        with open('alldata','wb') as fichier:
            picker = pickle.Pickler(fichier)
            picker.dump([self.chemin,self.car])
        print('Sauvegarde réussie')