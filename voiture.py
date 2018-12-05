class Voiture:
    def __init__(self, masse, longueur, largeur):
        self.masse = masse
        self.longueur = longueur
        self.largeur = largeur
        self.acceleration = []
        self.direction = []
        self.position = []

    def get_position(self, t):
        return self.position[t]

