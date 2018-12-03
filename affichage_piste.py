from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtWidgets, QtGui, QtCore
import piste


class Dessin(QWidget):

    def paintEvent(self, event):
        painter = QPainter(self)
        path1 = QPainterPath()
        path2 = QPainterPath()
        [pointx, pointy] = circuit.creationpiste(60)
        # a,b = min(pointx),min(pointy)
        path1.moveTo(abs(int(pointx[0].x)), abs(int(pointx[0].y)))
        path2.moveTo(abs(int(pointy[0].x)), abs(int(pointy[0].y)))
        for i in range(1, len(pointx)):
            path1.lineTo(abs(int(pointx[i].x)), abs(int(pointx[i].y)))
            path2.lineTo(abs(int(pointy[i].x)), abs(int(pointy[i].y)))
        painter.drawPath(path1)
        painter.drawPath(path2)


if __name__ == "__main__":
    app = QApplication([])
    win = QMainWindow()
    win.setCentralWidget(Dessin())
    win.showMaximized()
    app.exec_()
