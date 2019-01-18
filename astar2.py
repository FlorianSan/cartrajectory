import matplotlib.pyplot as plt
from heapq import heappush, heappop
from shapely.geometry import Point, Polygon, LineString
import numpy as np
import voiture
import piste

PASDETEMPS = 0.1  # en secondes


class Node:

    def __init__(self, vitesse, acceleration, direction, temps, dstart, dend, couttot, indexdend, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dstart = dstart
        self.dend = dend
        self.couttot = couttot
        
        self.indexdend = indexdend  # index du point de l'axe de piste le plus proche du noeud

        self.temps = temps  # nb de pas de temps pour arriver à ce noeud

        self.vitesse = vitesse
        self.direction = direction
        self.acceleration = acceleration

    def __eq__(self, autre):
        return self.position == autre.position

    def __repr__(self):
        return str(self.temps)


def astar(chemin, voit):

    coords = []  # coordonnées du polygone représentant la piste
    coordligneg = []  # coordonnées coté gauche de la piste
    coordligned = []  # coordonnée coté droit de la piste

    for i in range(len(chemin[1])):  # remplissage
        coords.append((chemin[1][i].x, chemin[1][i].y))
        coordligneg.append((chemin[1][i].x, chemin[1][i].y))

    for j in range(len(chemin[2])-1, 0, -1):  # remplissage
        coords.append((chemin[2][j].x, chemin[2][j].y))
        coordligned.append((chemin[2][j].x, chemin[2][j].y))

    polygon = Polygon(coords)  # création du polygone
    ligneg = LineString(coordligneg)  # création ligneg
    ligned = LineString(coordligned)  # création ligned
    lignefin = LineString([(chemin[1][-1].x, chemin[1][-1].y), (chemin[2][-1].x, chemin[2][-1].y)])  # ligne l'arrivée

    def newposition(currentnode):  # calcule les nouvelles positions à partir d'un noeud donné

        # deltavirage = voit.calculdeltavirage(currentnode.vitesse)  NE FONCTIONNE PAS
        deltavirage = voit.deltavirage

        for vir in range(-deltavirage, deltavirage + 1):
            newdirection = currentnode.direction + vir * voit.pasvirage

            for acc in range(-voit.deltaacc, voit.deltaacc + 1):
                newacceleration = currentnode.acceleration + acc * voit.pasacceleration
                newvitesse = currentnode.vitesse + PASDETEMPS * currentnode.acceleration

                if abs(newvitesse) > voit.vitessemax:
                    newvitesse = voit.vitessemax * np.sign(newvitesse)
                newposition = currentnode.position + piste.Point(-newvitesse * PASDETEMPS * np.sin(newdirection), newvitesse * PASDETEMPS * np.cos(newdirection))
                
                if abs(newvitesse)<abs(current_node.vitesse):
                    print('OK')
                ligne = LineString([(currentnode.position.x, currentnode.position.y), (newposition.x, newposition.y)])

                if (polygon.contains(Point(newposition.x, newposition.y)) and (not ligned.intersects(ligne) or not ligneg.intersects(ligne))) or ligne.intersects(lignefin):
                    temps = currentnode.temps + 1
                    dstart = currentnode.dstart + newvitesse * PASDETEMPS

                    if current_node.indexdend + 20 >= len(chemin[0]):
                        indexdend = len(chemin[0]) - 1
                    else:
                        indexdend = current_node.indexdend+20

                    while indexdend > 0 and chemin[0][indexdend].distance(newposition) > 2 * piste.LARGEUR:
                        indexdend -= 1
                    dend = chemin[0][indexdend].distance(newposition) + longueur.get(indexdend)
                    couttot = dstart + dend
                    newnode = Node(newvitesse, newacceleration, newdirection, temps, dstart, dend, couttot, indexdend, currentnode, newposition)
                    heappush(heap, (newnode.couttot, newnode))

    longueur = {}  # création d'un dictionnaire de longueur de la piste à patir de la fin
    longueur[len(chemin[0]) - 1] = 0

    for l in range(len(chemin[0]) - 2, -1, -1):
        longueur[l] = longueur.get(l + 1) + chemin[0][l].distance(chemin[0][l + 1])

    # création du noeud de debut
    start_node = Node(0, 0, directioninit(chemin[0][1], chemin[0][0]), 0, 0, longueur.get(0), longueur.get(0), len(chemin[0])-1, None, chemin[0][1],)

    # liste des noeuds a traiter  FILE DE PRIORITE
    heap = []

    # Ajoute le noeud de depart
    heappush(heap, (start_node.couttot, start_node))

    i = 0  # compteur (pour vérifier que l'algorithme tourne bien)

    # On boucle jusqu'au noeud final
    while heap:  # tant qu'il y a des noeuds a traiter

        current_node = heappop(heap)[1]

        # test fin
        if len(heap) > 1 and piste.intersect(current_node.parent.position, current_node.position, chemin[1][-1], chemin[2][-1]):
            position, acceleration, direction, vitesse = [], [], [], []

            while current_node is not None:  # on remonte l'arbre par la fin
                position.append(current_node.position)
                acceleration.append(current_node.acceleration)
                direction.append(current_node.direction)
                vitesse.append(current_node.vitesse)
                current_node = current_node.parent

            # mise à jour des caractéristiques de la voiture
            voit.position = position[::-1]
            voit.acceleration = acceleration[::-1]
            voit.vitesse = vitesse[::-1]
            voit.direction = direction[::-1]
            return None

        newposition(current_node)

        print(i)
        i += 1


def directioninit(point1, point2):  # détermination de la direction initiale en fonction du pt 0 et 1 de l'axe de piste
    dx, dy = point1.x-point2.x, point1.y-point2.y
    if dx > 0:
        return -np.arctan(dy / dx) + np.pi

    elif dx < 0:
        if dy > 0:
            return np.arctan(dx / dy)

        elif dy < 0:
            return np.arctan(dx / dy) + np.pi

        else:
            return 3 * np.pi / 2
    else:
        if dy > 0:
            return 0

        else:
            return np.pi
