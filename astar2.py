import piste


class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dstart = 0
        self.dend = 0
        self.couttot = 0

    def __eq__(self, autre):
        return self.position == autre.position


def astar(chemin, start, end):
    # crée le noeud de début et de fin
    start_node = Node(None, start)
    start_node.dstart = start_node.dend = start_node.couttot = 0
    end_node = Node(None, end)
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
            if item.couttot < current_node.couttot:
                current_node = item
                current_index = index

        # On retire le current node de la liste des noeuds à traiter et on l'ajoute dans la liste des noeuds traités
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Si on a atteint la fin
        if current_node == end_node:
            path = []  # initialise le chemin
            current = current_node
            while current is not None:  # on crée le chemin en partant de la fin
                path.append(current.position)
                current = current.parent
            return path[::-1]  # return le chemin inversé

        # Génère les children
        children = []
        for new_position in chemin.neighbors(current_node) :

            # On obtient la position du noeud A MODIFIER
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range A MODIFIER
            #if node_position[0] > (len(piste) - 1) or node_position[0] < 0 or node_position[1] > (len(piste[len(piste)-1]) -1) or node_position[1] < 0:
            #    continue

            # Noeud bien dans la piste
            for i in range(len(chemin.piste.pointsg)):
                if not piste.intersect(current_node.position[0],node_position[0],chemin.piste.pointsg[i],chemin.piste.pointsg[i+1])and not piste.intersect(current_node.position[0],node_position[0],chemin.piste.pointsd[i],chemin.piste.pointsd[i+1]) :
                    continue

            # Crée un nouveau noeud
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # On boucle sur les children
        for child in children:

            # Child est dans la liste des noeuds traités
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create couttot, dstart, dend
            child.dstart = current_node.dstart + 1    # 1 à modifier
            child.dend = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1])** 2)
            child.couttot = child.dstart + child.dend

            # Child dans la liste des noeuds à traiter
            for open_node in open_list:
                if child == open_node and child.dstart > open_node.dstart:
                    continue

            # Ajoute child dans open liste
            open_list.append(child)
