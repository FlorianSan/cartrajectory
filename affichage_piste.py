#affichage
import math

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPen, QBrush, QColor

import piste

WIDTH = 800  # Initial window width (pixels)
HEIGHT = 450  # Initial window height (pixels)
AIRPORT_Z_VALUE = 0
APT_COLOR = "black"


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
        self.view = PanZoomView(self.scene)
        self.time_entry = QtWidgets.QLineEdit()

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
        track_group.setZValue(AIRPORT_Z_VALUE)

        [pointx, pointy] = piste.creationpiste(600)

        pen = QPen(QtGui.QColor(APT_COLOR), 40)
        pen.setCapStyle(QtCore.Qt.RoundCap)

        path = QtGui.QPainterPath()

        path.moveTo(abs(int(pointx[0].x)), abs(int(pointx[0].y)))

        for i in range(1, len(pointx)):
            path.lineTo(abs(int(pointx[i].x)), abs(int(pointx[i].y)))
        item = QtWidgets.QGraphicsPathItem(path, track_group)
            #item = QtWidgets.QGraphicsPathItem(path2, airport_group)
        item.setPen(pen)





