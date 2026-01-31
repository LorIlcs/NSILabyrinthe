"""
Contient les asserts pour la vérification
de la classe Labyrinthe, Graphe et Parcours
"""

from random import randrange
try:
    from .labyrinthe import *
    from .graphe_dico import Graphe
    from .parcours_graphe import *
except ImportError:
    from labyrinthe import *
    from graphe_dico import Graphe
    from parcours_graphe import *

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

# case_valide

laby1 = Labyrinthe(long=8, larg=6)
laby2 = Labyrinthe(long=5, larg=11)

for laby in (laby1, laby2):
    for L in range(laby.larg):
        assert laby.case_valide(0, L)
        assert not laby.case_valide(-1, L)

    for C in range(laby.long):
        assert laby.case_valide(C, 0)
        assert not laby.case_valide(C, -1)

    for L in range(laby.larg):
        assert laby.case_valide(laby.long - 1, L)
        assert not laby.case_valide(laby.long, L)

    for C in range(laby.long):
        assert laby.case_valide(C, laby.larg -1)
        assert not laby.case_valide(C, laby.larg)
        
valide("case_valide")

# mur_valide

for laby in (laby1, laby2):
    for y in range(laby.larg):
        assert laby.mur_valide(0, y, 0, y + 1)
        assert not laby.mur_valide(-1, y, -1, y + 1)
    for y in range(laby.larg + 1):
        assert laby.mur_valide(0, y, 1, y)
        assert not laby.mur_valide(-1, y, 0, y)

    for x in range(laby.long + 1):
        assert laby.mur_valide(x, 0, x, 1)
        assert not laby.mur_valide(x, -1, x, 0)
    for x in range(laby.long):
        assert laby.mur_valide(x, 0, x + 1, 0)
        assert not laby.mur_valide(x, -1, x + 1, -1)

    for y in range(laby.larg):
        assert laby.mur_valide(laby.long, y, laby.long, y + 1)
        assert not laby.mur_valide(laby.long + 1, y, laby.long + 1, y + 1)
    for y in range(laby.larg + 1):
        assert laby.mur_valide(laby.long -1, y, laby.long, y)
        assert not laby.mur_valide(laby.long, y, laby.long + 1, y)

    for x in range(laby.long + 1):
        assert laby.mur_valide(x, laby.larg - 1, x, laby.larg)
        assert not laby.mur_valide(x, laby.larg, x, laby.larg + 1)
    for x in range(laby.long):
        assert laby.mur_valide(x, laby.larg, x + 1, laby.larg)
        assert not laby.mur_valide(x, laby.larg + 1, x + 1, laby.larg + 1)


    for _ in range(laby.long * laby.larg // 4):
        x0 = randrange(2, laby.long - 2)
        y0 = randrange(2, laby.larg - 2)
        x1 = x0 + randrange(-2, 3)
        y1 = y0 + randrange(-2, 3)
        dif = (x1 - x0, y1 - y0)
        correct = (dif in [(1, 0), (0, 1)])
        assert laby.mur_valide(x0, y0, x1, y1) == correct
valide("mur_valide")

# Graphe
# ================================

vide = Graphe()
assert vide.adj == dict()
valide("Graphe.__init__")

# arc
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
valide("Graphe.arc")

# ajouter_sommet, ajouter_arc
essai.ajouter_sommet("E")
essai.ajouter_arc("A", "B")
essai.ajouter_arc("B", "A")
assert "E" in essai.adj
assert essai.adj["B"] == {"A"}
valide("Graphe.ajouter_sommet et ajouter_arc")

# sommets, voisins
assert "A" in essai.sommets()
assert "E" in essai.sommets()
assert essai.voisins("A") == {"B", "C", "D"}
assert essai.voisins("B") == {"A"}
valide("Graphe.sommets et voisins")

# antecedents
DICO_ANT = { "A": {"B", "C"},
             "B": {"A"},
             "C": {"A"} }
essai_ant = Graphe()
essai_ant.adj = DICO_ANT
assert essai_ant.antecedents("A") == {"B", "C"}
assert essai_ant.antecedents("B") == {"A"}
assert essai_ant.antecedents("C") == {"A"}
valide("Graphe.antecedents")

# est_symetrique, symetrise
assert not essai.est_symetrique()
essai_sym = essai.clone()
essai_sym.symetrise()
assert essai_sym.est_symetrique()
valide("Graphe.est_symetrique et symetrise")

# clone
essai_clone = essai.clone()
assert essai_clone == essai
assert essai_clone is not essai
essai_clone.ajouter_arc("E", "A")
assert essai_clone != essai
valide("Graphe.clone")

# existe_chemin_rec, existe_chemin_pile, parcours_largeur, distance, court_chemin
g_test = Graphe()
for i in range(5):
    g_test.ajouter_sommet(i)

g_test.ajouter_arc(0, 1)
g_test.ajouter_arc(1, 2)
g_test.ajouter_arc(2, 3)
g_test.ajouter_arc(3, 4)
g_test.ajouter_arc(1, 0)
g_test.ajouter_arc(3, 1)

# existe_chemin_rec
assert existe_chemin_rec(g_test, 0, 1)
assert existe_chemin_rec(g_test, 0, 4)
assert existe_chemin_rec(g_test, 1, 3)
assert not existe_chemin_rec(g_test, 4, 0)
valide("existe_chemin_rec")

# existe_chemin_pile
assert existe_chemin_pile(g_test, 0, 1)
assert existe_chemin_pile(g_test, 0, 4)
assert existe_chemin_pile(g_test, 1, 3)
assert not existe_chemin_pile(g_test, 4, 0)
valide("existe_chemin_pile")

# parcours_largeur
dist = parcours_largeur(g_test, 0)
assert dist[0] == 0
assert dist[1] == 1
assert dist[2] == 2
assert dist[3] == 3
assert dist[4] == 4
valide("parcours_largeur")

# distance
assert distance(g_test, 0, 0) == 0
assert distance(g_test, 0, 1) == 1
assert distance(g_test, 0, 4) == 4
assert distance(g_test, 4, 0) is None
valide("distance")

# court_chemin
chemin = court_chemin(g_test, 0, 4)
assert chemin is not None
assert chemin[0] == 0
assert chemin[-1] == 4
assert len(chemin) == 5
chemin_invalide = court_chemin(g_test, 4, 0)
assert chemin_invalide is None
valide("court_chemin")

# murs_case
laby_test = Labyrinthe(long=5, larg=5)
murs_0_0 = laby_test.murs_case(0, 0)
assert (0, 0, 1, 0) in murs_0_0
assert (0, 1, 1, 1) in murs_0_0
assert (0, 0, 0, 1) in murs_0_0
assert (1, 0, 1, 1) in murs_0_0
assert len(murs_0_0) == 4

murs_invalide = laby_test.murs_case(10, 10)
assert murs_invalide == set()
valide("murs_case")

# cases_mur
cases_mur_h = laby_test.cases_mur(0, 0, 1, 0)
assert (0, 0) in cases_mur_h
assert len(cases_mur_h) >= 1
assert (0, -1) not in cases_mur_h

cases_mur_v = laby_test.cases_mur(0, 0, 0, 1)
assert (0, 0) in cases_mur_v
assert len(cases_mur_v) >= 1

cases_invalide = laby_test.cases_mur(10, 10, 11, 10)
assert cases_invalide == set()
valide("cases_mur")

# passe_muraille
laby_passage = Labyrinthe(long=3, larg=3, murs=set())
assert laby_passage.passe_muraille(0, 0, 1, 0)
assert laby_passage.passe_muraille(0, 0, 0, 1)
assert laby_passage.passe_muraille(1, 1, 2, 1)

laby_mur = Labyrinthe(long=3, larg=3, murs={(1, 0, 1, 1)})
assert not laby_mur.passe_muraille(0, 0, 1, 0)
assert laby_mur.passe_muraille(0, 0, 0, 1)

try:
    laby_passage.passe_muraille(10, 10, 11, 11)
    assert False, "Should raise IndexError"
except IndexError:
    pass
valide("passe_muraille")

# construit_graphe
laby_graphe = Labyrinthe(long=3, larg=3, murs=set())
g = laby_graphe.construit_graphe()

for x in range(3):
    for y in range(3):
        assert (x, y) in g.sommets()
assert len(g.sommets()) == 9

assert (1, 0) in g.voisins((0, 0))
assert (0, 1) in g.voisins((0, 0))
assert (0, 0) in g.voisins((1, 0))
assert (0, 0) in g.voisins((0, 1))

laby_graphe_mur = Labyrinthe(long=3, larg=3, murs={(1, 0, 1, 1)})
g_mur = laby_graphe_mur.construit_graphe()
assert not laby_graphe_mur.passe_muraille(0, 0, 1, 0)
assert (1, 0) not in g_mur.voisins((0, 0))
assert (0, 0) not in g_mur.voisins((1, 0))
assert (0, 1) in g_mur.voisins((0, 0))
assert (0, 0) in g_mur.voisins((0, 1))


assert g_mur.est_symetrique()
valide("construit_graphe")

# =====================================
#  RÉSUMÉ DES TESTS
# =====================================

print("\n" + "="*60)
print("Bravo! Tous les tests sont passés avec succès!")
print("="*60)
print("\n" + "="*60)
 
