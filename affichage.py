from PyQt5.QtWidgets import QGraphicsEllipseItem

class CarItem(QGraphicsEllipseItem):
    """The view of an car in the GraphicsScene"""

    def __init__(self, simu, f):
        """CarItem constructor, creates the ellipse and adds to the scene"""
        super().__init__(None)
        self.setZValue(radarview.PLOT_Z_VALUE)

        # instance variables
        self.flight = f
        self.simulation = simu
        # build the ellipse
        width = 10
        self.setRect(-width, -width, width * 2, width * 2)
        # add tooltip
        tooltip = f.type.name + ' ' + f.call_sign + ' ' + f.qfu
        self.setToolTip(tooltip)

    def mousePressEvent(self, event):
        """Overrides method in QGraphicsItem for interaction on the scene"""
        # Do nothing for the moment...
        event.accept()

    def update_position(self, is_conflict):
        """moves the plot in the scene"""
        position = self.flight.get_position(self.simulation.t)
        self.setBrush(DEP_BRUSH if self.flight.type == traffic.Movement.DEP else ARR_BRUSH)
        if is_conflict:
            self.setBrush(CONF_BRUSH)
        self.setPos(position.x, position.y)