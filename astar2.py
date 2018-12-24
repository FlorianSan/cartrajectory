import matplotlib.pyplot as plt

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

        self.vitesse = vitesse
        self.direction = direction
        self.acceleration = acceleration

    def __eq__(self, autre):
        return self.position == autre.position

M = 0
L = 0
Lg = 0

# rajouter affichage


def astar(chemin, start):
    voit = voiture.Voiture(M, L, Lg)
    # crée le noeud de début et de fin
    start_node = Node(0, 0, 0, None, start)
    start_node.dstart = 0
    start_node.dend = ((start_node.position.x - chemin[-1][0].x) ** 2 + (start_node.position.y - chemin[-1][0].y) ** 2)**0.5
    start_node.couttot = 0

    # Initialisation des deux listes
    open_list = []  # liste des noeuds à traiter  FILE DE PRIORITÉ
    closed_list = []  # liste des noeuds déjà traités

    # Ajoute le noeud de départ
    open_list.append(start_node)

    # On boucle jusqu'au noeud final
    while len(open_list) > 0:  # tant qu'il y a des noeuds à traiter


        # Accéder au noeud courant
        for i in range(1, len(open_list)):
            if open_list[i-1].couttot > open_list[i].couttot:
                open_list[i-1], open_list[i] = open_list[i], open_list[i-1]
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.dend < current_node.dend :
                current_node = item
                current_index = index


        # On retire le current node de la liste des noeuds à traiter et on l'ajoute dans la liste des noeuds traités
        open_list.pop(current_index)
        closed_list.append(current_node)

        print(current_node.position.x, current_node.position.y)

        # Génère les children
        children = []

        res = voiture.newposition(current_node.vitesse, current_node.acceleration, current_node.direction, current_node.position)
        for i in range(len(res)):
            children.append(Node(res[i][2], res[i][1], res[i][3], current_node, res[i][0]))

            verif=True # Test si child se trouve dans la piste
            for i in range(len(chemin[1])-1):
                if piste.intersect(current_node.position, children[-1].position, chemin[1][i], chemin[1][i+1])or piste.intersect(current_node.position, children[-1].position, chemin[2][i], chemin[2][i+1]):
                    verif=False
            if not verif:
                children.pop()



        # Si on a atteint la fin
        for child in children:
            if piste.intersect(current_node.position, child.position, chemin[1][-1], chemin[2][-1]):
                print('OK')
                path = []  # initialise le chemin
                current = current_node
                while current is not None:  # on crée le chemin en partant de la fin
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # return le chemin

        # On boucle sur les children
        for child in children:

            # Child est dans la liste des noeuds traités
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create coutrest, dstart, dend
            child.dstart = current_node.dstart + 1
            child.dend = ((child.position.x - chemin[0][-1].x) ** 2 + (child.position.y - chemin[1][-1].y) ** 2)**0.5 # A modifier (doit dépendre du temps)
            child.couttot = child.dstart + child.dend

            # Child dans la liste des noeuds à traiter
            #  for open_node in open_list:
            #    if child == open_node and child.dstart > open_node.dstart:
            #        continue
            # Ajoute child dans open liste
            open_list.append(child)


chemin = piste.creationpiste(100)

def afficherpiste(l1, l2):
    for k in range(len(l1)-1):
        a = [l1[k].x, l1[k+1].x]
        b = [l1[k].y, l1[k + 1].y]
        c = [l2[k].x, l2[k + 1].x]
        d = [l2[k].y, l2[k + 1].y]
        plt.plot(a, b)
        plt.plot(c,d)
        plt.axis('equal')



afficherpiste(chemin[1],chemin[2])

ast=astar(chemin, chemin[0][0])


def afficherastar(l1):
    for k in range(len(l1) - 1):
        a = [l1[k].x, l1[k + 1].x]
        b = [l1[k].y, l1[k + 1].y]
        plt.plot(a, b)
        plt.axis('equal')
    plt.show()

afficherastar(ast)
