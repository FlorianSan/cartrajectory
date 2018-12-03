from PyQt5.QtWidgets import QGraphicsEllipseItem
import voiture
import affichage_piste
class CarItem(QGraphicsEllipseItem):
    """The view of an car in the GraphicsScene"""

    def __init__(self, car):
        """CarItem constructor, creates the ellipse and adds to the scene"""
        super().__init__(None)
        self.setZValue(affichage_piste.PLOT_Z_VALUE)

        # instance variables
        self.car = car

        # build the ellipse
        width = 10
        self.setRect(-width, -width, width * 2, width * 2)


    def mousePressEvent(self, event):
        """Overrides method in QGraphicsItem for interaction on the scene"""
        # Do nothing for the moment...
        event.accept()

    def update_position(self):
        """moves the plot in the scene"""
