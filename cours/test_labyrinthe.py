"""
Contient les asserts pour la vérification
de la classe Labyrinthe
"""

from random import randrange
from labyrinthe import *

# ===========================
#    Préparation des tests
#============================

ANNONCE = """
************************************************************************
************************************************************************
**                                                                    **
**                                                                    **
**          Les tests sur la classe Labyrinthe sont en cours          **
**                                                                    **
**                                                                    **
************************************************************************
************************************************************************

"""

def valide(nom_methode):
    """
    Envoie à l'écran que la méthode dont le nom est donné
    en paramètre a été validée
    """
    

    texte = f"! La méthode: {nom_methode} semble correcte !"
    bord = "!" * len(texte)
    blanc = "!" + " "*(len(texte) - 2) + "!"
    print()
    print(bord)
    print(blanc)
    print(texte)
    print(blanc)
    print(bord,"\n")

print(ANNONCE)

# ================================
# Tests de la méthode: case_valide
# ================================

laby1 = Labyrinthe(long=8, larg=6)
laby2 = Labyrinthe(long=5, larg=11)

for laby in (laby1, laby2):
    # Tests sur le bord gauche
    for L in range(laby.larg):
        assert laby.case_valide(0, L)
        assert not laby.case_valide(-1, L)

    # Test sur le bord haut
    for C in range(laby.long):
        assert laby.case_valide(C, 0)
        assert not laby.case_valide(C, -1)

    # Tests sur le bord droit
    for L in range(laby.larg):
        assert laby.case_valide(laby.long - 1, L)
        assert not laby.case_valide(laby.long, L)

    # Test sur le bord bas
    for C in range(laby.long):
        assert laby.case_valide(C, laby.larg -1)
        assert not laby.case_valide(C, laby.larg)
        
valide("case_valide")

# ================================
# Tests de la méthode: mur_valide
# ================================

for laby in (laby1, laby2):
    # Tests sur le bord gauche (vers le bas) 
    for y in range(laby.larg):
        assert laby.mur_valide(0, y, 0, y + 1)
        assert not laby.mur_valide(-1, y, -1, y + 1)
    # Tests sur le bord gauche (vers la droite)
    for y in range(laby.larg + 1):
        assert laby.mur_valide(0, y, 1, y)
        assert not laby.mur_valide(-1, y, 0, y)

    # Tests sur le bord haut (vers le bas)
    for x in range(laby.long + 1):
        assert laby.mur_valide(x, 0, x, 1)
        assert not laby.mur_valide(x, -1, x, 0)
    # Tests sur le bord haut (vers la droite)
    for x in range(laby.long):
        assert laby.mur_valide(x, 0, x + 1, 0)
        assert not laby.mur_valide(x, -1, x + 1, -1)

    # Tests sur le bord droit (vers le bas) 
    for y in range(laby.larg):
        assert laby.mur_valide(laby.long, y, laby.long, y + 1)
        assert not laby.mur_valide(laby.long + 1, y, laby.long + 1, y + 1)
    # Tests sur le bord droit (vers la droite)
    for y in range(laby.larg + 1):
        assert laby.mur_valide(laby.long -1, y, laby.long, y)
        assert not laby.mur_valide(laby.long, y, laby.long + 1, y)

    # Tests sur le bord bas (vers le bas)
    for x in range(laby.long + 1):
        assert laby.mur_valide(x, laby.larg - 1, x, laby.larg)
        assert not laby.mur_valide(x, laby.larg, x, laby.larg + 1)
    # Tests sur le bord bas (vers la droite)
    for x in range(laby.long):
        assert laby.mur_valide(x, laby.larg, x + 1, laby.larg)
        assert not laby.mur_valide(x, laby.larg + 1, x + 1, laby.larg + 1)

    # Tests aléatoires
    for _ in range(laby.long * laby.larg // 4):
        x0 = randrange(2, laby.long - 2)
        y0 = randrange(2, laby.larg - 2)
        x1 = x0 + randrange(-2, 3)
        y1 = y0 + randrange(-2, 3)
        dif = (x1 - x0, y1 - y0)
        correct = (dif in [(1, 0), (0, 1)])
        assert laby.mur_valide(x0, y0, x1, y1) == correct
valide("mur_valide")
 
