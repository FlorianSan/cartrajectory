# affichage
import math

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import  QTimer, Qt
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QWidget, QLabel, QLineEdit


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
    # repris de aéroport
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
    def __init__(self,chemin, car):
        super().__init__()

        # Settings
        self.setWindowTitle('Trajectoire')
        self.resize(WIDTH, HEIGHT)


        self.car = car
        self.chemin = chemin
        self.piste = chemin[0]
        # create components
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('green'))
        self.view = PanZoomView(self.scene)
        self.time_entry = QtWidgets.QLineEdit()

        self.moving_car = affichage.CarMotion(self, self.car)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.moving_car.updateValues)

        toolbar = self.create_toolbar()
        self.add_piste()

        # add components to the root_layout
        root_layout.addWidget(self.view)
        root_layout.addLayout(toolbar)
        self.show()



    def create_toolbar(self):
        # pris de aéroport
        generaltoolbar = QtWidgets.QVBoxLayout()
        toolbar = QtWidgets.QHBoxLayout()
        generaltoolbar.addLayout(toolbar)
        self.label = QtWidgets.QLabel(self)
        generaltoolbar.addWidget(self.label)
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
        add_button('R', self.moving_car.redemarrer)
        add_button('Save Track', lambda: self.sauvegarder('sansA'))
        add_button('Save Simu', lambda: self.sauvegarder('avecA'))
        toolbar.addStretch()

        def add_shortcut(text, slot):
            """creates an application-wide key binding"""
            shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(text), self)
            shortcut.activated.connect(slot)

        add_shortcut('+', lambda: self.view.zoom_view(1.1))
        add_shortcut('-', lambda: self.view.zoom_view(1 / 1.1))
        add_shortcut(' ', self.playpause)
        add_shortcut('R', self.moving_car.redemarrer)
        add_shortcut('s', lambda: self.sauvegarder('AvecA'))
        add_shortcut('q', QtCore.QCoreApplication.instance().quit)
        return generaltoolbar

    def add_piste(self):
        #création des éléments de la piste
        track_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(track_group)

        pen = QPen(QtGui.QColor(TK_COLOR), LARGEUR)
        pen.setJoinStyle(Qt.RoundJoin)
        self.extrem(4)

        path = QtGui.QPainterPath()
        path.moveTo(self.piste[0].x, self.piste[0].y)
        for i in range(1, len(self.piste)):
            path.lineTo(self.piste[i].x, self.piste[i].y)
        item = QtWidgets.QGraphicsPathItem(path, track_group)
        item.setPen(pen)
        
            
    def extrem(self,nb):
        #création de nb lignes de carrés à l'arrivée et au départ
        deltax, deltay = self.piste[nb+1].x-self.piste[0].x,self.piste[nb+1].y-self.piste[0].y
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
        #crée un quatrième point pour faire un losange
        Deltax,Deltay=Point1.x-Point2.x,Point1.y-Point2.y
        P4=piste.Point(Point3.x+Deltax,Point3.y+Deltay)
        return(Point3,P4)
        
    def dessin(self,point1, point2, pointpiste1,pointpiste2,nb):
        #dessin de ligne de carrés entre point1 et point2
        Deltax,Deltay=(point1.x-point2.x),(point1.y-point2.y)
        deltax,deltay=pointpiste1.x-pointpiste2.x,pointpiste1.y-pointpiste2.y
        v=math.sqrt(deltax**2+deltay**2)
        V2=LARGEUR/10
        pen = QPen(QtGui.QColor('white'),V2)
        pen.setCapStyle(Qt.SquareCap)
        pen.setJoinStyle(Qt.RoundJoin)
        if v!=0:
            deltax,deltay=deltax/v,deltay/v
        if nb==1:
            for i in range(1,5):
                P1=piste.Point(point1.x-i*Deltax/5,point1.y-i*Deltay/5)
                P2=piste.Point(point1.x -i*Deltax/5 + V2*deltax*0.5,point1.y -i*Deltay/5+V2*deltay*0.5)
                self.scene.addLine(P1.x,P1.y,P2.x,P2.y,pen)
        else:
            for i in range(5):
                P1=piste.Point(point1.x-(2*i+1)*Deltax/10,point1.y-(2*i+1)*Deltay/10)
                P2=piste.Point(point1.x-(2*i+1)*Deltax/10 + V2*deltax*0.5,point1.y -(2*i+1)*Deltay/10+V2*deltay*0.5)
                self.scene.addLine(P1.x,P1.y,P2.x,P2.y,pen)

            
    @QtCore.pyqtSlot()
    def playpause(self):
        self.label.setText("")
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(33)
            
    def sauvegarder(self,style):
        self.savedata=SAVEDATA(style,self.chemin,self.car)
        self.savedata.show()

class SAVEDATA(QWidget):
    #permet de sauvegarder la piste et/ou la simulation entière en fonction de style qui peut être 'sansA' ou 'avecA'
    def __init__(self,style,chemin,voiture):
        super().__init__()
        #récupère les données à sauvegarder
        self.chemin = chemin
        self.car = voiture
        self.style= style
        #paramètres
        self.label = QLabel('nom fichier',self)
        self.nom = QLineEdit('',self)
        button = QPushButton("Save")
        button.clicked.connect(self.savename)
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        hbox.addWidget(self.nom)
        hbox.addWidget(button)
        self.setLayout(hbox)
        self.setFixedSize(300, 50)
        self.setWindowTitle('Choix data')
        self.show()

    def savename(self):
        #crée le nom et appelle la bonne fonction pour sauvegarder
        self.close()
        name=str(self.nom.text())
        if self.style == 'sansA':
            filename = './DATA/'+name
            self.sauvegarder(filename)
        else:
            filename = './DATAstar/'+name
            self.savesimu(filename)

    def sauvegarder(self,filename):
        #sauvegarde uniquement la piste dans le dossier DATA
        try:
            with open(filename,'wb') as fichier:
                mon_picker=pickle.Pickler(fichier)
                mon_picker.dump(self.chemin)
            print("Sauvegarde réussie ")
            self.label.setText("Sauvegarde réussie ")
        except:
            print("Echec sauvegarde ")
            self.label.setText("Echec sauvegarde ")



    def savesimu(self,filename):
        #sauvegarde la simulation dans le dossier DATAstar
        try:
            with open(filename,'wb') as fichier:
                picker = pickle.Pickler(fichier)
                picker.dump([self.chemin,self.car])
            print('Sauvegarde réussie')
            self.label.setText("Sauvegarde réussie ")
        except:
            print("Echec sauvegarde ")
            self.label.setText("Echec sauvegarde ")