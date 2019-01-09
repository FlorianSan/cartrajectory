import sys, math
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSignal, Qt



import piste
import affichage

class MouseTracker(QWidget):
    listeMouseTracker = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Dessin Piste')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.pos = None
        self.pointsm = [piste.Point(0, 0)]  # liste des points milieux

    def mouseMoveEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:

            self.pointsm.append(piste.Point(event.x(), event.y()))
            self.update()

    def paintEvent(self, event):

        q = QPainter(self)
        if len(self.pointsm)>=1:
            for i in range(len(self.pointsm)-1):
                q.drawLine(self.pointsm[i].x, self.pointsm[i].y, self.pointsm[i+1].x,self.pointsm[i+1].y)

            if self.pos :
                q.drawLine(self.pointsm[len(self.pointsm)-1].x, self.pointsm[len(self.pointsm)-1].y,  self.pos.x(),  self.pos.y())

    def closeEvent(self, event):

        self.listeMouseTracker.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MouseTracker()
    ex.show()
    sys.exit(app.exec_())