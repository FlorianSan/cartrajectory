import matplotlib.pyplot as plt
import numpy as np
import random as rd

LARGEUR = 15  # en mètre
PAS = 15  # en mètreS
NBETAPEZONE = 5  # nb étapes avant le choix d'une nouvelle zone
NBZONE = 24  # nb de zones
ANGLEZONE = 360 // NBZONE  # en degré
INTENSITEVIRAGE = 4  # plus cette valeur est importante et plus les virages auront tendance à être serrés
LIMITECADRE = 10000


def afficherpiste2(l1, l2):
    for k in range(len(l1)):
        a = [l1[k].x, l2[k].x]
        b = [l1[k].y, l2[k].y]
        print(k)
        plt.plot(a, b)
        plt.axis('equal')
    plt.show()


def afficherpiste(l1, l2):
    for k in range(len(l1) - 1):
        a = [l1[k].x, l1[k + 1].x]
        b = [l1[k].y, l1[k + 1].y]
        c = [l2[k].x, l2[k + 1].x]
        d = [l2[k].y, l2[k + 1].y]
        print(k)
        plt.plot(a, b)
        plt.plot(c, d)
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
    # return False
    if a == d and b == c:
        return True
    else:
        return (a != c and a != d and b != c and b != d and clockwise(a, b, c) != clockwise(a, b, d) and clockwise(a, c,
                                                                                                                   d) != clockwise(
            b, c, d))


class Piste:

    def __init__(self):
        self.pointsx = [Point(0, +LARGEUR / 2)]  # liste de points
        self.pointsy = [Point(0, -LARGEUR / 2)]  # liste de points
        self.pointsm = [Point(0, 0)]  # liste des points milieux
        self.zone = [0]  # initialisation à 0 nécessaire afin que le début de la piste soit rectiligne
        self.angle = 0  # en degré
        self.anglerad = 0  # en rad (nécessaire pour les calculs)

    def miseajourzone(self):
        self.zone.append(rd.randint(self.zone[-1] - INTENSITEVIRAGE, self.zone[-1] + INTENSITEVIRAGE))

    def miseajourangle(self):
        self.angle = rd.randint(0, ANGLEZONE) + ANGLEZONE * self.zone[-1]
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
            if intersect(pointx, self.pointsx[i], pointy, self.pointsy[i]):
                verif = False
        return verif

    def ajoutpoint(self, pointx, pointy):
        self.pointsx.append(pointx)
        self.pointsy.append(pointy)


def creationpiste(nbiterations):
    piste = Piste()
    i = 0
    piste.zone = [0]  # initialisation nécessaire afin que le début de la piste soit rectiligne
    z = len(piste.zone)

    while i < nbiterations:
        while len(piste.pointsx) - z * NBETAPEZONE < NBETAPEZONE:
            piste.miseajourangle()
            piste.miseajourpointm()
            px, py = piste.creationpointspiste()
            if piste.verificationpoint(px, py) and veriflimitecadre(px, py):
                piste.ajoutpoint(px, py)
                i = i + 1
                # print(i)
            else:
                l = len(piste.pointsm)
                print("l=" + str(l))
                print("lpiste=" + str(len(piste.zone)))
                print(l - (len(piste.zone) + 2) * NBETAPEZONE)
                for k in range(l - (len(piste.zone) + 2) * NBETAPEZONE + 1):
                    piste.pointsm.pop()
                    piste.pointsx.pop()
                    piste.pointsy.pop()
                    # print("CHEVAUCHEMENT")
                    i = i - 1
                piste.zone.pop()
                piste.zone.pop()
                z = z - 2
        # print(piste.zone)
        piste.miseajourzone()
        z = z + 1
    return piste.pointsm


if __name__ == "__main__":
    def afficherpiste(l1):
        for k in range(len(l1) - 1):
            a = [l1[k].x, l1[k + 1].x]
            b = [l1[k].y, l1[k + 1].y]
            # c = [l2[k].x, l2[k+1].x]
            # d = [l2[k].y, l2[k+1].y]
            print(k)
            plt.plot(a, b)
            # plt.plot(c,d)
            plt.axis('equal')
        plt.show()


    pm = creationpiste(1000)
    afficherpiste(pm)
