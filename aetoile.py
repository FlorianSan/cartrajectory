class Path:
    def __init__(self, nodes, totalCost):
        self.nodes = nodes
        self.totalCost = totalCost

    def getNodes(self):
        return self.nodes

    def getTotalMoveCost(self):
        return self.totalCost


class Node:
    def __init__(self, location, mCost, lid, parent=None):
        self.location = location  # où est situé le noeud dans l'arbre
        self.mCost = mCost  # coût total pour attiendre ce noeud
        self.parent = parent  # parent du noeud
        self.score = 0  # score calculé pour ce noeud ?????
        self.lid = lid  # met en place un id de localisation pour chaque loc sur la carte

    def __eq__(self, n):  # fonction 'est égale à'
        if n.lid == self.lid:
            return 1
        else:
            return 0


class AStar:

    def __init__(self, maphandler):  # gestionnaire de map ???????
        self.mh = maphandler

    def _getBestOpenNode(self):  # obtient le meilleur noeud pas encore calculé
        bestNode = None
        for n in self.on:  # pour chaque dans la liste de noeuds à traiter
            if not bestNode:
                bestNode = n
            else:
                if n.score <= bestNode.score:
                    bestNode = n
        return bestNode

    def _tracePath(self, n):  # trace le chemin en remontant l'arbre
        nodes = []
        totalCost = n.mCost  # cout total = cout tot du noeud
        p = n.parent
        nodes.insert(0, n)  # ajoute le noeud en début de liste

        while 1:  # tant que l'id == n
            if p.parent is None:  # si en haut de liste (pas de parent)
                break

            nodes.insert(0, p)  # on met le parent de début de liste des noeuds
            p = p.parent

        return Path(nodes, totalCost)

    def _handleNode(self, node, end):  # fction qui gère chaque noeud
        i = self.o.index(node.lid)  # index du noeud dans la liste des noeuds à traiter
        self.on.pop(i)  # on supprime ce noeud des noeuds courants
        self.o.pop(i)  # on le supprime des noeuds à traiter
        self.c.append(node.lid)  # on l'aoute dans la liste des noeuds traités

        nodes = self.mh.getAdjacentNodes(node, end)  # fction getAdjacentNodes ???????

        for n in nodes:  # pour chaque noeud
            if n.location == end:  # on a atteint la destination
                return n
            elif n.lid in self.c:  # déjà dans la liste des noeuds traités, on continue
                continue
            elif n.lid in self.o:  # déjà dans la liste des noeuds à traiter, on vérifie si il y a pas de meilleur score
                i = self.o.index(n.lid)
                on = self.on[i]  # on prend la valeur du noeud courant d'indice i
                if n.mCost < on.mCost:  # si le noeud à traiter a un cout plus faible que le noeud courant
                    self.o.pop(i)  # on supprime l'indice du noeud à traiter
                    self.on.append(n)  # n devient un noeud courant (dans liste d'ouverts)
                    self.o.append(n.lid)  # on ajoute l'id de n à la liste des noeuds à traiter
            else:  # si c'est un nouveau noeud, on l'ajoute à la liste des noeuds à traiter
                self.on.append(n)
                self.o.append(n.lid)

        return None

    def findPath(self, fromlocation, tolocation):
        self.o = []  # id des noeuds à traiter
        self.on = []  # valeur des noeuds à traiter
        self.c = []  # déjà étudiés

        end = tolocation
        fnode = self.mh.getNode(fromlocation)  # noeuds de la map en la position fromlocation
        self.on.append(fnode)  # on ajoute ce noeud dans la liste des noeuds à traiter
        self.o.append(fnode.lid)  # ...
        nextNode = fnode  # fnode devient le prochain noeud

        while nextNode is not None:  # tant qu'on a pas tout parcouru
            finish = self._handleNode(nextNode, end)  # le début devient le nextnode
            if finish:  # si on a finit
                return self._tracePath(finish)  # on trace le chemin
            nextNode = self._getBestOpenNode()  # le next noeud est le best node suivant

        return None


class SQ_Location:
    """A simple Square Map Location implementation"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, l):
        """MUST BE IMPLEMENTED"""
        if l.x == self.x and l.y == self.y:
            return 1
        else:
            return 0


class SQ_MapHandler:  ##inutile pour l'instant
    """A simple Square Map implementation"""

    def __init__(self, mapdata, width, height):
        self.m = mapdata
        self.w = width
        self.h = height

    def getNode(self, location):
        """MUST BE IMPLEMENTED"""
        x = location.x
        y = location.y
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return None
        d = self.m[(y * self.w) + x]
        if d == -1:
            return None

        return Node(location, d, ((y * self.w) + x))

    def getAdjacentNodes(self, curnode, dest):
        """MUST BE IMPLEMENTED"""
        result = []

        cl = curnode.location
        dl = dest

        n = self._handleNode(cl.x + 1, cl.y, curnode, dl.x, dl.y)
        if n: result.append(n)
        n = self._handleNode(cl.x - 1, cl.y, curnode, dl.x, dl.y)
        if n: result.append(n)
        n = self._handleNode(cl.x, cl.y + 1, curnode, dl.x, dl.y)
        if n: result.append(n)
        n = self._handleNode(cl.x, cl.y - 1, curnode, dl.x, dl.y)
        if n: result.append(n)

        return result

    def _handleNode(self, x, y, fromnode, destx, desty):
        n = self.getNode(SQ_Location(x, y))
        if n is not None:
            dx = max(x, destx) - min(x, destx)
            dy = max(y, desty) - min(y, desty)
            emCost = dx + dy
            n.mCost += fromnode.mCost
            n.score = n.mCost + emCost
            n.parent = fromnode
            return n

        return None
