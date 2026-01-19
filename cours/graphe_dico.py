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
                   
    
            
   
if __name__ == "__main__":
    
    # ====================================
    # Vérification de la méthode __init__
    # ====================================
    
                     
    vide = Graphe()
    assert vide.adj == dict()
   
    print("La méthode __init__ semble correcte")
    
    # ======================================
    # Vérification de la méthode arc
    # ======================================
    
    DICO = { "A": {"B", "C", "D"},
             "B": set(),
             "C": {"A"},
             "D": {"A", "C"} }
                
    essai = Graphe()
    essai.adj = DICO
    
    assert essai.arc("A", "B")
    assert essai.arc("A", "C")
    assert essai.arc("A", "D")
    assert not essai.arc("B", "A")
    assert not essai.arc("B", "C")
    assert not essai.arc("B", "D")
    assert essai.arc("C", "A")
    assert not essai.arc("C", "B")
    assert not essai.arc("C", "D")
    assert essai.arc("D", "A")
    assert not essai.arc("D", "B")
    assert essai.arc("D", "C")
        
    print("La méthode arc semble correcte")
    
    # =========================================
    # Vérification de la méthode ajouter_sommet
    # =========================================
    
    for lettre in "ABCD":
        assert lettre in essai.adj
    assert not "E" in essai.adj
    assert len(essai.adj) == 4
    
    essai.ajouter_sommet("D")
    assert essai.arc("D", "A")
    assert not essai.arc("D", "B")
    assert essai.arc("D", "C")
    
    essai.ajouter_sommet("E")
    for lettre in "ABCD":
        assert not essai.arc("E", lettre)
    assert len(essai.adj) == 5
    
    print("La méthode ajouter_sommet semble correcte")
    
    # ======================================
    # Vérification de la méthode ajouter_arc
    # ======================================
    
    essai.ajouter_arc("A", "B")
    assert essai.adj["A"] == {"B", "C", "D"}
    
    essai.ajouter_arc("B", "A")
    assert essai.adj["B"] == {"A"}
    
    essai.ajouter_arc("C", "D")
    assert essai.adj["C"] == {"A", "D"}
    
    essai.ajouter_arc("E", "F")
    assert essai.adj["E"] == {"F"}
    assert essai.adj["F"] == set()
    
    essai.ajouter_arc("F", "E")
    assert essai.adj["E"] == {"F"}
    assert essai.adj["F"] == {"E"}
    
    essai.ajouter_arc("G", "H")
    assert essai.adj["G"] == {"H"}
    assert essai.adj["H"] == set()
    
    assert len(essai.adj) == 8
    
    print("La méthode ajouter_arc semble correcte")

    # =================================
    # Vérification de la méthode __eq__
    # =================================

    DICO = { "A": {"B", "C", "D"},
             "B": {"A"},
             "C": {"A", "D"},
             "D": {"A", "C"},
             "E": {"F"},
             "F": {"E"},
             "G": {"H"},
             "H": set()}
             
    essai_1 = essai
    assert essai_1 == essai
    
    essai_2 = Graphe()
    essai_2.adj = DICO
    assert essai_2 == essai
    
    essai_2.ajouter_arc("D", "A")
    assert essai_2 == essai
    essai_2.ajouter_arc("D", "B")
    assert not essai_2 == essai
    
    print("La méthode __eq__ semble correcte")

    # ================================
    # Vérification de la méthode clone
    # ================================
    
    essai1 = essai.clone()
    assert essai1 == essai
    assert not essai1 is essai
    essai1.ajouter_arc("H", "A")
    assert essai1 != essai

    print("La méthode clone semble correcte")

    # ==================================
    # Vérification de la méthode sommets
    # ==================================

    assert essai.sommets() == set("ABCDEFGH")

    print("La méthode sommets semble correcte")

    
    # ==================================
    # Vérification de la méthode voisins
    # ==================================
    
    assert essai.voisins("A") == {"B", "C", "D"}
    assert essai.voisins("B") == {"A"}
    assert essai.voisins("C") == {"A", "D"}
    assert essai.voisins("D") == {"A", "C"}
    assert essai.voisins("E") == {"F"}
    assert essai.voisins("F") == {"E"}
    assert essai.voisins("G") == {"H"}
    assert essai.voisins("H") == set()

    print("La méthode voisins semble correcte")
    
    # ======================================
    # Vérification de la méthode antecedents
    # ======================================
    DICO = { "A": {"B", "C", "D"},
             "B": {"A"},
             "C": {"A", "H"},
             "D": {"A", "C"},
             "E": {"F"},
             "F": {"E", "G"},
             "G": {"H"},
             "H": set()}

    essai = Graphe()
    essai.adj = DICO
    assert essai.antecedents("A") == set("BCD")
    assert essai.antecedents("B") == set("A")
    assert essai.antecedents("C") == set("AD")
    assert essai.antecedents("D") == set("A")
    assert essai.antecedents("E") == set("F")
    assert essai.antecedents("F") == set("E")
    assert essai.antecedents("G") == set("F")
    assert essai.antecedents("H") == set("CG")
    
    print("La méthode antecedents semble correcte")
    
    # =========================================
    # Vérification de la méthode est_symetrique
    # =========================================
    
    assert not essai.est_symetrique()

    DICO_S = { "A": {"B", "C", "D"},
             "B": {"A"},
             "C": {"A", "D"},
             "D": {"A", "C"},
             "E": {"F"},
             "F": {"E"},
             "G": {"H"},
             "H": {"G"} }

    essai1 = Graphe()
    essai1.adj = DICO_S
    assert essai1.est_symetrique()

    print("La méthode est_symetrique semble correcte")

    # ====================================
    # Vérification de la méthode symetrise
    # ====================================
    
    g2 = essai.clone()
    g2.symetrise()
    assert g2.est_symetrique()
    
    
    print("La méthode symetrise semble correcte")
    
    # Conclusion
    
    print("Bravo! Toutes les méthodes semblent correctes")
                          
    
