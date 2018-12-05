from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen
from PyQt5 import QtWidgets, QtGui, QtCore
import math

from PyQt5.QtWidgets import QApplication, QMainWindow

import piste
import affichage



WIDTH = 800  # Initial window width (pixels)
HEIGHT = 450  # Initial window height (pixels)
AIRPORT_Z_VALUE = 0
COLOR = "black"


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

        [point] = piste.creationpiste(600)
        (a,b)=minimum(point)
        pen = QPen(QtGui.QColor(COLOR), 20)
        pen.setCapStyle(QtCore.Qt.RoundCap)

        path = QtGui.QPainterPath()

        path.moveTo(point[0].x-a, point[0].y-b)

        for i in range(1, len(point)):
            path.lineTo(point[i].x-a, point[i].y-b)
        item = QtWidgets.QGraphicsPathItem(path, track_group)
        item.setPen(pen)

def minimum(liste):
    a = liste[0].x
    b = liste[0].y
    for i in range(1,len(liste)):
        if liste[i].x<a:
            a=liste[i].x
        elif liste[i].y<b:
            b=liste[i].y
    return(a,b)

if __name__ == "__main__":
    app = QApplication([])
    win = QMainWindow()
    win.setCentralWidget(Dessin())
    win.showMaximized()
    app.exec_()
