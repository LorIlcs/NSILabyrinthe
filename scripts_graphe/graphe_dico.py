"""
Graphe représenté par un dictionnaire d'adjacence
"""

class Graphe:
    """
    Un graphe aura un seul attribut un dictionnaire:
    les clés sont les noms des sommets
    les valeurs sont l'ensemble des sommets adjacents
    """
    
    def __init__(self):
        """
        Création d'un graphe vide
        """
        
        self.adj = dict()
        
        
    def arc(self, s1, s2):
        """
        Renvoie True si et seulement si l'arc s1 --> s2 existe
        """
        
        return s2 in self.adj[s1]
        
        
    def ajouter_sommet(self, s):
        """
        Ne fait rien si le sommet s existe déjà
        Sinon ajoute la clé s dans adj avec pour valeur un ensemble vide
        """
        
        if s not in self.adj:
            self.adj[s] = set()

            
            
    def ajouter_arc(self, s1, s2):
        """
        Crée les sommets s1 et s2 si necessaire
        puis ajoute le sommet s2 dans l'ensemble des adjacents
        associé à s1
        """
        
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1].add(s2)


    def __eq__(self, other):
        """
        Les 2 graphes sont égaux si et seulement si
        leur dictionnaire d'adjacence sont égaux
        """
        
        return self.adj == other.adj
    
        
    def clone(self):
        """
        Renvoie une copie du graphe.
        Les dictionnaires d'adjacence contiennent les mêmes valeurs
        mais sont des objets indépendants
        """
        
        copie = Graphe()
        for som, vois in self.adj.items():
            copie.ajouter_sommet(som)
            for v in vois:
                copie.ajouter_arc(som, v)
        return copie

        
    def sommets(self):
        """
        Renvoie l'ensemble des sommets du graphe
        """
        
        return set(self.adj)
    
        
    def voisins(self, s):
        """
        Renvoie l'ensemble des voisins du sommet s
        """
        
        return self.adj[s]
    
            
    def antecedents(self, t):
        """
        Renvoie l'ensemble des antecedents du sommet t
        C'est à dire tous les sommets s tels qu'il existe
        un arc reliant s à t
        """

        #sortie = set()
        #for s in self.adj:
        #    if t in self.adj[s]:
        #       sortie.add(s)
        #return sortie

        return {s for s in self.adj if t in self.adj[s]}


    def est_symetrique(self):
        """
        Renvoie True si le graphe est symétrique
        C'est à dire, s'il existe un arc qui relie u et v
        alors il existe aussi un arc qui relie v et u
        """

        for s in self.adj:
            if self.voisins(s) != self.antecedents(s):
                return False
        return True           


    def symetrise(self):
        """
        Modifie sur place le graphe en ajoutant si necessaire
        l'arc (v, u) lorsque l'arc (u, v) existe.
        """

        for s in self.adj:
            for v in self.voisins(s):
                self.ajouter_arc(v, s)