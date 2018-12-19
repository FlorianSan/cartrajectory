import piste
import voiture


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


def astar(chemin, start, end):
    voit = voiture.Voiture(M, L, Lg)
    # crée le noeud de début et de fin
    start_node = Node(0, 0, 0, None, start)
    start_node.dstart = start_node.dend = start_node.couttot = 0
    end_node = Node(0, 0, 0, None, end)   # tout modifier pour pouvoir enlever ça
    end_node.dend = end_node.dstart = end_node.couttot = 0

    # Initialisation des deux listes
    open_list = []  # liste des noeuds à traiter
    closed_list = []  # liste des noeuds déjà traités

    # Ajoute le noeud de départ
    open_list.append(start_node)

    # On boucle jusqu'au noeud final
    while len(open_list) > 0:  # tant qu'il y a des noeuds à traiter

        # Accéder au noeud courant
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.couttot < current_node.couttot:  # rajouter couttot
                current_node = item
                current_index = index

        # On retire le current node de la liste des noeuds à traiter et on l'ajoute dans la liste des noeuds traités
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Génère les children
        children = []

        # Si on a atteint la fin
        for child in children:
            if piste.intersect(current_node.position, child.position, chemin.piste.pointsg[-1], chemin.piste.pointsd[-1]):
                path = []  # initialise le chemin
                current = current_node
                while current is not None:  # on crée le chemin en partant de la fin
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # return le chemin

        for new_position in voiture.newposition(current_node.vitesse, current_node.acceleration, current_node.direction, current_node.position)[3]:  # a mod
            # On obtient la position du noeud
            node_position = new_position

            # Crée un nouveau noeud
            res = voiture.newposition(current_node.vitesse, current_node.acceleration, current_node.direction, current_node.position)
            for i in range(len(res)):
                children.append(Node(res[i][2], res[i][1], res[i][3], current_node, res[i][0]))

            for i in range(len(chemin.piste.pointsg)):
                if piste.intersect(current_node.position, node_position, chemin.piste.pointsg[i], chemin.piste.pointsg[i+1])or piste.intersect(current_node.position, node_position, chemin.piste.pointsd[i], chemin.piste.pointsd[i+1]):
                    children.pop()
                    continue

        # On boucle sur les children
        for child in children:

            # Child est dans la liste des noeuds traités
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create coutrest, dstart, dend
            child.dstart = current_node.dstart + 1    # 1 à modifier
            child.dend = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)**0.5
            child.couttot = child.dstart + child.dend

            # Child dans la liste des noeuds à traiter
            #  for open_node in open_list:
            #    if child == open_node and child.dstart > open_node.dstart:
            #        continue

            # Ajoute child dans open liste
            open_list.append(child)
