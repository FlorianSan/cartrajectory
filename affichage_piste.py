# affichage
import math

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF
from PyQt5.QtWidgets import QApplication
import sys

import pickle
import piste
import affichage
import mouse_tracker
import astar2

LARGEUR = piste.LARGEUR
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


        self.car = car


        if choice == 1:
            self.chemin = piste.creationpiste(20)
            self.lancerastar()
            self.ready = True

        elif choice == 2:
            with open('data','rb') as fichier:
                mon_depickler=pickle.Unpickler(fichier)
                self.chemin  = mon_depickler.load()
                self.lancerastar()
                self.ready =True
                
        elif choice == 3:
            with open('alldata','rb') as fichier:
                depickler = pickle.Unpickler(fichier)
                [self.chemin,self.car] = depickler.load()
                self.mainwindows()
                self.ready = True
        else:

            self.ex = mouse_tracker.MouseTracker()
            self.ex.listeMouseTracker.connect(self.listemousetracker)
            self.ex.setWindowModality(QtCore.Qt.ApplicationModal)
            self.ex.show()
    
    def lancerastar(self):
        astar2.astar(self.chemin, self.car)
        self.mainwindows()

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

        self.view.scale(-1, 1)

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
        add_button(' - ', lambda: self.view.zoom_view(0.9))
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

        add_shortcut('+', lambda: self.zoom_view(1.1))
        add_shortcut('-', lambda: self.zoom_view(1 / 1.1))
        add_shortcut(' ', self.playpause)
        add_shortcut('R', self.redemarrer)
        add_shortcut('P',self.sauvegarder)
        add_shortcut('q', QtCore.QCoreApplication.instance().quit)
        return toolbar

    def add_piste(self):

        track_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(track_group)

        pen = QPen(QtGui.QColor(TK_COLOR), LARGEUR)
        pen.setCapStyle(QtCore.Qt.RoundCap)

        path = QtGui.QPainterPath()

        path.moveTo(self.piste[0].x, self.piste[0].y)
        self.scene.addPolygon(Polygonee(self.chemin[1][0], self.chemin[2][0], self.piste[1],self.piste[2], 20), QPen(QtGui.QColor(TK_COLOR), 1), QBrush(QColor(TK_COLOR)))
        self.scene.addRect(self.piste[0].x, self.piste[0].y - 3.5*LARGEUR/9, 5, LARGEUR/9, QPen(QtGui.QColor(TK_COLOR), 0.5), QBrush(QColor('white')))
        self.scene.addRect(self.piste[0].x, self.piste[0].y - 1.5*LARGEUR/9, 5, LARGEUR/9, QPen(QtGui.QColor(TK_COLOR), 0.5), QBrush(QColor('white')))
        self.scene.addRect(self.piste[0].x, self.piste[0].y + 0.5*LARGEUR/9, 5, LARGEUR/9, QPen(QtGui.QColor(TK_COLOR), 0.5), QBrush(QColor('white')))
        self.scene.addRect(self.piste[0].x, self.piste[0].y + 2.5*LARGEUR/9, 5, LARGEUR/9, QPen(QtGui.QColor(TK_COLOR), 0.5), QBrush(QColor('white')))
        for i in range(1, len(self.piste)):
            path.lineTo(self.piste[i].x, self.piste[i].y)
        self.scene.addPolygon(Polygonee(self.chemin[1][-1],self.chemin[2][-1],self.piste[-1],self.piste[-2], 20), QPen(QtGui.QColor(TK_COLOR), 1), QBrush(QColor(TK_COLOR)))
        item = QtWidgets.QGraphicsPathItem(path, track_group)
        item.setPen(pen)

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
        print(self.chemin)
        self.lancerastar()
        self.ready = True

    def miseajour(self):
        if self.ready:
            self.moving_car.updateValues()

    def savesimu(self):
        with open('alldata','wb') as fichier:
            picker = pickle.Pickler(fichier)
            picker.dump([self.chemin,self.car])
        print('Sauvegarde réussie')

def Polygone(A, B, longueur):
    theta = math.atan((B.y - A.y) / (B.x - A.x))
    B1 = QPoint(B.x - LARGEUR * math.sin(theta) / 2, B.y + LARGEUR * math.cos(theta) / 2)
    B2 = QPoint(B.x + LARGEUR * math.sin(theta) / 2, B.y - LARGEUR * math.cos(theta) / 2)
    C = piste.Point(B.x + longueur * (B.x - A.x), B.y + longueur * (B.y - A.y))
    C1 = QPoint(C.x - LARGEUR * math.sin(theta) / 2, C.y + LARGEUR * math.cos(theta) / 2)
    C2 = QPoint(C.x + LARGEUR * math.sin(theta) / 2, C.y - LARGEUR * math.cos(theta) / 2)
    Poly = QPolygonF()
    lt = [B1, B2, C2, C1]
    for i in range(len(lt)):
        Poly.append(lt[i])
    return (Poly)
    
def Polygonee(A,B,C,D,longueur):
    deltax,deltay=C.x-D.x,C.y-D.y
    P1=QPoint(A.x,A.y)
    P2=QPoint(A.x+longueur*deltax,A.y+longueur*deltay)
    P3=QPoint(B.x+longueur*deltax,B.y+longueur*deltay)
    P4=QPoint(B.x,B.y)
    Poly = QPolygonF()
    lt = [P1,P2,P3,P4]
    for i in range(4):
        Poly.append(lt[i])
    return(Poly)