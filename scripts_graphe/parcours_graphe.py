"""
Parcours d'un graphe
"""

try:
    from .graphe_dico import Graphe
except ImportError:
    from graphe_dico import Graphe

def parcours_profondeur_rec(g, vus, s):
    """
    Parcours en profondeur du graphe g depuis le sommet s
    vus est l'ensemble des sommets déjà parcourus.
    Version récursive
    """

    if s not in vus:
        vus.add(s)
        for v in g.voisins(s):
            parcours_profondeur_rec(g, vus, v)


def existe_chemin_rec(g, u, v):
    """
    Renvoie True s'il existe un chemin allant de u à v 
    en suivant les arcs du graphe g
    Utilise la version récursive
    """
    
    vus = set()
    parcours_profondeur_rec(g, vus, u)
    return v in vus


def parcours_profondeur_pile(g, vus, s):
    """
    Parcours en profondeur du graphe g depuis le sommet s
    vus est l'ensemble des sommets déjà parcourus.
    Version utilisant une pile
    """

    pile = [s]
    while pile:
        t = pile.pop()
        if t not in vus:
            vus.add(t)
            for v in g.voisins(t):
                pile.append(v)


def existe_chemin_pile(g, u, v):
    """
    Renvoie True s'il existe un chemin allant de u à v 
    en suivant les arcs du graphe g
    utilise la version avec pile
    """
    
    vus = set()
    parcours_profondeur_pile(g, vus, u)
    return v in vus

    

BLANC, GRIS, NOIR = 1, 2, 3


def parcours_cy(g, couleur, s):
    """
    Parcours en profondeur depuis le sommet s 
    dans le but de déterminer la présence ou non d'un cycle.
    Renvoie True si et seulement s'il existe
    un cycle dans un parcours commençant par le sommet s
    """
    
    if couleur[s] == GRIS:
        return True
    if couleur[s] == NOIR:
        return False
    couleur[s] = GRIS
    for v in g.voisins(s):
        if parcours_cy(g, couleur, v):
            return True
    couleur[s] = NOIR
    return False
        


def cycle(g):
    """
    Renvoie True si et seulement si le graphe g donné en paramètre
    contient au moins un cycle
    """

    couleur = dict()
    for s in g.sommets():
        couleur[s] = BLANC
    for s in g.sommets():
        if parcours_cy(g, couleur, s):
            return True
    return False


def parcours_largeur(g, s):
    """
    Parcours en largeur le graphe g depuis le sommet s
    Renvoie un dictionnaire de couples
    sommet: distance de s à ce sommet
    """

    dist = {s: 0}
    actuel, suivant = {s}, set()

    while actuel:
        t = actuel.pop()
        dist_suivant = dist[t] + 1
        for v in g.voisins(t):
            if v not in dist:
                suivant.add(v)
                dist[v] = dist_suivant
        if not actuel:
            actuel, suivant = suivant, set()
    return dist


def distance(g, u, v):
    """
    Renvoie la distance du sommet u au sommet v
    dans le graphe g
    Renvoie None s'il n'y a pas de chemin
    """

    dist = parcours_largeur(g, u)
    return dist.get(v, None)


def court_chemin(g, u, v):
    """
    Renvoie la liste des sommets de l'un des plus courts chemins
    reliant u à v dans l'ordre de parcours : {u, s1, s2, ..., v}
    Renvoie None si un tel chemin n'existe pas
    """

    dist = parcours_largeur(g, u)
    if v not in dist:
        return None
    long = dist[v]
    court = [v]
    actuel = v
    while long > 0:
        long -= 1
        prec = {t for t in g.antecedents(actuel) if dist.get(t, -1) == long}
        s = prec.pop()
        court = [s] + court
        actuel = s
    return court
