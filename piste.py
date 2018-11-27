import matplotlib.pyplot as plt
import numpy as np
import random as rd

LARGEUR = 15  # en mètre
PAS = 10  # en mètre
NBETAPEZONE = 5  # nb étapes avant le choix d'une nouvelle zone
NBZONE = 24  # nb de zones
ANGLEZONE = 360 // NBZONE  # en degré
INTENSITEVIRAGE = 3  # plus cette valeur est importante et plus les virages auront tendance à être serrés


def afficherpiste(l1, l2):
    for k in range(len(l1)):
        a = [l1[k].x, l2[k].x]
        b = [l1[k].y, l2[k].y]
        print(k)
        plt.plot(a, b)
        plt.axis('equal')
    plt.show()


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def clockwise(a, b, c):
    x1 = b.x - a.x
    y1 = b.y - a.y
    x2 = c.x - a.x
    y2 = c.y - a.y
    return x1 * y2 - x2 * y1 < 0


def intersect(a, b, c, d):
    if a == d and b == c:
        return True
    else:
        return (a != c and a != d and b != c and b != d and clockwise(a, b, c) != clockwise(a, b, d) and clockwise(a, c,
                                                                                                                   d) != clockwise(
            b, c, d))


class Piste:

    def __init__(self):
        self.largeur = LARGEUR
        self.pas = PAS
        self.pointsx = [Point(0, -LARGEUR / 2)]  # liste de points
        self.pointsy = [Point(0, +LARGEUR / 2)]  # liste de points
        self.pointsm = [Point(0, 0)]  # liste des points milieux
        self.zone = 0  # initialisation à 0 nécessaire afin que le début de la piste soit rectiligne
        self.angle = 0  # en degré
        self.anglerad = 0  # en rad (nécessaire pour les calculs)

    def miseajourzone(self):
        self.zone = rd.randint(self.zone - INTENSITEVIRAGE, self.zone + INTENSITEVIRAGE)

    def miseajourangle(self):
        self.angle = rd.randint(0, ANGLEZONE) + ANGLEZONE * self.zone
        self.anglerad = self.angle * np.pi / 180

    def miseajourpointm(self):
        self.pointsm.append(
            Point(self.pointsm[-1].x - PAS * np.cos(self.anglerad), self.pointsm[-1].y + PAS * np.sin(self.anglerad)))

    def creationpointspiste(self):
        pointx = Point(self.pointsm[-1].x + LARGEUR / 2 * np.sin(self.anglerad),
                       self.pointsm[-1].y + LARGEUR / 2 * np.cos(self.anglerad))
        pointy = Point(self.pointsm[-1].x - LARGEUR / 2 * np.sin(self.anglerad),
                       self.pointsm[-1].y - LARGEUR / 2 * np.cos(self.anglerad))

        return pointx, pointy

    def verificationpoint(self, pointx, pointy):
        verif = True
        for i in range(len(self.pointsx)):
            if intersect(pointx, pointy, self.pointsx[i], self.pointsy[i]):
                verif = False
        return verif

    def ajoutpoint(self, pointx, pointy):
        self.pointsx.append(pointx)
        self.pointsy.append(pointy)


def creationpiste(nbiterations):
    piste = Piste()
    N = 0
    i = 0
    piste.zone = 0  # initialisation nécessaire afin que le début de la piste soit rectiligne
    while i < nbiterations:
        while N < NBETAPEZONE:
            piste.miseajourangle()
            piste.miseajourpointm()
            px, py = piste.creationpointspiste()
            if piste.verificationpoint(px, py):
                piste.ajoutpoint(px, py)
                N = N + 1
                i = i + 1
                print(i)
        N = 0
        piste.miseajourzone()
    afficherpiste(piste.pointsx, piste.pointsy)

creationpiste(600)