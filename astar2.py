import matplotlib.pyplot as plt
import numpy as np

import piste
import voiture
from operator import itemgetter, attrgetter


class Node:

    def __init__(self, vitesse, acceleration, direction, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dstart = 0
        self.dend = 0
        self.couttot = 0

        self.temps = 0  # nb de pas de temps pour arriver à ce noeud

        self.vitesse = vitesse
        self.direction = direction
        self.acceleration = acceleration

    def __eq__(self, autre):
        return self.position == autre.position


M = 0
L = 0
Lg = 0


# rajouter affichage


def astar(chemin):
    compteur = 0

    voit = voiture.Voiture(M, L, Lg)
    # cree le noeud de debut et de fin
    start_node = Node(0, 0, np.pi, None, chemin[0][0])
    start_node.dstart = 0
    l = -1
    d = chemin[0][l].distance(chemin[0][l - 1])
    while chemin[0][l].distance(start_node.position) > piste.LARGEUR:
        start_node.dend += d
        l = l - 1
    # start_node.dend = ((start_node.position.x - chemin[-1][0].x) ** 2 +v(start_node.position.y - chemin[-1][0].y) ** 2) ** 0.5
    start_node.couttot = start_node.dstart + start_node.dend

    # Initialisation des deux listes
    open_list = []  # liste des noeuds a traiter  FILE DE PRIORITe
    closed_list = []  # liste des noeuds deja traites

    # Ajoute le noeud de depart
    open_list.append(start_node)

    # On boucle jusqu'au noeud final
    while len(open_list) > 0:  # tant qu'il y a des noeuds a traiter

        # Acceder au noeud courant
        for i in range(1, len(open_list)):
            if open_list[i - 1].couttot > open_list[i].couttot:
                open_list[i - 1], open_list[i] = open_list[i], open_list[i - 1]
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.couttot < current_node.couttot:
                current_node = item
                current_index = index

        # On retire le current node de la liste des noeuds a traiter et on l'ajoute dans la liste des noeuds traites
        open_list.pop(current_index)
        closed_list.append(current_node)

        #print(current_node.position.x, current_node.position.y)

        compteur += 1
        print(compteur)

        # Genere les children
        children = []

        res = voiture.newposition(current_node.vitesse, current_node.acceleration, current_node.direction,
                                  current_node.position)
        for i in range(len(res)):
            children.append(Node(res[i][2], res[i][1], res[i][3], current_node, res[i][0]))
            children[-1].temps = current_node.temps + 1

            verif = True  # Test si child se trouve dans la piste
            for j in range(len(chemin[1]) - 1):
                if piste.intersect(current_node.position, children[-1].position, chemin[1][j],
                                   chemin[1][j + 1]) or piste.intersect(current_node.position, children[-1].position,
                                                                        chemin[2][j], chemin[2][j + 1]):
                    verif = False
            if not verif:
                children.pop()
        if len(children) == 0:
            open_list.pop(0)

        # Si on a atteint la fin
        
        listendnode=[]
        for child in children :
            if piste.intersect(current_node.position, child.position, chemin[1][-1], chemin[2][-1]):
                listendnode.append(child)
        if len(listendnode)>0:
            print(len(listendnode))
            endchild=listendnode[0]
            difdir=abs(current_node.direction-endchild.direction)
            for child in listendnode :
                if difdir> abs(child.direction-current_node.direction):
                    endchild=child
                    difdir=abs(child.direction-current_node.direction)
            #print('OK')
            path = []  # initialise le chemin
            current = endchild
            while current is not None:  # on cree le chemin en partant de la fin
                path.append(current.position)
                current = current.parent
            return path[::-1]  # return le chemin 
        

        # On boucle sur les children
        for child in children:

            # Child est dans la liste des noeuds traites
            """for closed_child in closed_list:
                if child == closed_child:
                    continue"""

            # Create coutrest, dstart, dend
            child.dstart = current_node.dstart + child.vitesse * child.temps * voiture.PASDETEMPS

            l = -1
            while chemin[0][l].distance(child.position) > piste.LARGEUR:
                child.dend += chemin[0][l].distance(chemin[0][l - 1])
                l = l - 1
            child.dend += chemin[0][l].distance(child.position)

            child.couttot = child.dstart + child.dend

            open_list.append(child)





def afficherpiste(l1, l2):
    for k in range(len(l1) - 1):
        a = [l1[k].x, l1[k + 1].x]
        b = [l1[k].y, l1[k + 1].y]
        c = [l2[k].x, l2[k + 1].x]
        d = [l2[k].y, l2[k + 1].y]
        plt.plot(a, b)
        plt.plot(c, d)
        plt.axis('equal')







def afficherastar(l1):
    for k in range(len(l1) - 1):
        a = [l1[k].x, l1[k + 1].x]
        b = [l1[k].y, l1[k + 1].y]
        plt.plot(a, b)
        plt.axis('equal')
    plt.show()



if __name__ == "__main__":
    chemin = piste.creationpiste(300)
    afficherpiste(chemin[1], chemin[2])
    ast = astar(chemin)
    afficherastar(ast)