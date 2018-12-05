#affichage
import math 

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF

import piste

WIDTH = 800  # Initial window width (pixels)
HEIGHT = 450  # Initial window height (pixels)
AIRPORT_Z_VALUE = 0
TK_COLOR = "black"


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
    def __init__(self):
        super().__init__()
        self.time_increment = 1

        # Settings
        self.setWindowTitle('Trajectoire')
        self.resize(WIDTH, HEIGHT)

        # create components
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QColor('green'))
        self.view = PanZoomView(self.scene)
        self.time_entry = QtWidgets.QLineEdit()
        self.point = piste.creationpiste(600)

        # invert y axis for the view
        self.view.scale(1, -1)

        # add the airport elements to the graphic scene and then fit it in the view
        self.add_piste()


        # add components to the root_layout
        root_layout.addWidget(self.view)

        # show the window
        self.show()


    def add_piste(self):

        track_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(track_group)


        pen = QPen(QtGui.QColor(TK_COLOR), 15)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        
        path = QtGui.QPainterPath()
        point = self.point
        path.moveTo(point[0].x, point[0].y)
        
        self.scene.addRect(point[0].x,point[0].y-10,40,20,QPen(QtGui.QColor(TK_COLOR),1),QBrush(QColor('black')))
        for i in range(1, len(point)):
            path.lineTo(point[i].x, point[i].y)
        item = QtWidgets.QGraphicsPathItem(path, track_group)
        item.setPen(pen)