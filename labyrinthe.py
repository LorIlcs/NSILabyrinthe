"""
Outils pour la fabrication du graphe
d'un labyrinthe donné par ses murs
"""

from graphe_dico import *

class Labyrinthe():
    def __init__(self, long=4, larg=4, murs=set()):
        self.long = long
        self.larg = larg
        self.murs = murs
    
    def case_valide(self, C, L):
        """
        Renvoie True si et seulement si les coordonnées
        sont celles d'une case valide du labyrinthe
        """
        
        return C in range(self.long) and L in range(self.larg)
        
        
    def mur_valide(self, x0, y0, x1, y1):
        """
        Renvoie True si et seulement si les coordonnées
        sont celles d'un mur valide bien orienté
        """
        
        # Vérifie que les coordonnées 
        # font partie du labyrinthe
        for x in (x0, x1):
            if x not in range(self.long + 1):
                return False
        for y in (y0, y1):
            if y not in range(self.larg + 1):
                return False
                
        # Vérifie que le mur a une longueur 1
        cas_v = (x1 == x0 + 1) and (y1 == y0)
        cas_h = (x1 == x0) and (y1 == y0 + 1)
        return (cas_v or cas_h)      


    def murs_case(self, C, L):
        """
        Renvoie l'ensemble contenant les murs pouvant border la case
        """

        if not self.case_valide(C, L):
            return set()

        haut = (C, L, C + 1, L)
        bas = (C, L + 1, C + 1, L + 1)
        gauche = (C, L, C, L + 1)
        droite = (C + 1, L, C + 1, L + 1)
        return {haut, bas, gauche, droite}        


    def cases_mur(self, x0, y0, x1, y1):
        """
        Renvoie l'ensemble des cases bordant le mur
        """

        if not self.mur_valide(x0, y0, x1, y1):
            return set()

        cases = set()
        if (x1 - x0, y1 - y0) == (1, 0):
            # Le mur est horizontal
            case_h = (x0, y0 - 1)
            if self.case_valide(x0, y0 -1):
                cases.add(case_h)
            case_b = (x0, y0)
            if self.case_valide(x0, y0):
                cases.add(case_b)             
        else:
            # Le mur est vertical
            case_g = (x0 - 1, y0)
            if self.case_valide(x0 - 1, y0):
                cases.add(case_g)
            case_d = (x0, y0)
            if self.case_valide(x0, y0):
                cases.add(case_d)
        return cases  
        
    def passe_muraille(self, C0, L0, C1, L1):
        """
        Renvoie True si et seulement s'il n'y a pas de mur
        entre les cases (C0, L0) et (C1, L1)
        """

        if not (self.case_valide(C0, L0) and self.case_valide(C1, L1)):
            raise IndexError("cases invalide") # cas de base à l'ecterieur du laby

        murs_0 = self.murs_case(C0, L0)
        murs_1 = self.murs_case(C1, L1)

        
        murs_proches = murs_0 & murs_1
        
        
        for mur in murs_proches:
            if mur in self.murs:
                return False 

        return True


        
    def construit_graphe(self):
        # Construit des sommets pour le graphe
        laby = Graphe()
        
        for x in range(self.long): # on parcour toute les cases qui deviennent des sommet
            for y in range(self.larg):
                laby.ajouter_sommet((x, y))
                
        # pour les arcs de notre labyrinthe
        # on parcour toute les cases encore pour voir qui sont les voisins et mettre les arcs
        for x in range(self.long):   
            for y in range(self.larg):

                if x + 1 < self.long: # case de droite 
                    if self.passe_muraille(x, y, x + 1, y): # je verifie avec passe_muraille si il y pas de mur entre eux
                        laby.ajouter_arc((x, y), (x + 1, y)):# si il y a pas de mur ajoute un arc au graphe

                if y + 1 < self.larg: # case du bas
                    if self.passe_muraille(x, y, x, y + 1): # meme chose
                        laby.ajouter_arc((x, y), (x, y + 1)):

        return laby
                                         

                              
                    

    
                
        
        
if __name__ == "__main__":
    import test_labyrinthe 
                
#=================
#   VERIFICATION
#=================
            
laby = Labyrinthe(long=8, larg=4)

# mur_valide
#assert laby.mur_valide(0, 0, 1, 0)      # horrizontal
#assert laby.mur_valide(0, 0, 0, 1)      # verticall
#assert laby.mur_valide(7, 3, 8, 3)
#assert laby.mur_valide(7, 3, 7, 4)
#assert not laby.mur_valide(0, 0, 2, 0)  # trp long
#assert not laby.mur_valide(0, 0, 0, 2)
#assert not laby.mur_valide(-1, 0, 0, 0)
#assert not laby.mur_valide(0, -1, 0, 0)
#assert not laby.mur_valide(8, 0, 9, 0)
#assert not laby.mur_valide(0, 4, 0, 5)

# Pour case_valide
assert laby.case_valide(0, 0)
assert laby.case_valide(7, 3)
assert not laby.case_valide(8, 0)
assert not laby.case_valide(0, 4)
# assert
