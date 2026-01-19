import tkinter as tk

def grille_cliquable(canvas, L, H, taille_case=40):
    """
    Dessine un quadrillage cliquable :
    - chaque côté de chaque case est indépendant
    - clic : bascule plein <-> pointillé
    """

    def basculer(event):
        segment = canvas.find_withtag("current")[0]

        if "pointille" in canvas.gettags(segment):
            canvas.itemconfig(segment, dash=())
            canvas.dtag(segment, "pointille")
            canvas.addtag_withtag("plein", segment)
        else:
            canvas.itemconfig(segment, dash=(4, 4))
            canvas.dtag(segment, "plein")
            canvas.addtag_withtag("pointille", segment)

    def creer_segment(x1, y1, x2, y2, plein=True):
        dash = () if plein else (4, 4)
        etat = "plein" if plein else "pointille"

        segment = canvas.create_line(
            x1, y1, x2, y2,
            width=2,
            dash=dash,
            tags=("arete", etat)
        )
        canvas.tag_bind(segment, "<Button-1>", basculer)

    largeur = L * taille_case
    hauteur = H * taille_case

    for i in range(L):
        for j in range(H):
            x = i * taille_case
            y = j * taille_case

            # Haut
            creer_segment(x, y, x + taille_case, y, plein=True)
            # Bas
            creer_segment(x, y + taille_case, x + taille_case, y + taille_case, plein=True)
            # Gauche
            creer_segment(x, y, x, y + taille_case, plein=True)
            # Droite
            creer_segment(x + taille_case, y, x + taille_case, y + taille_case, plein=True)

fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, width=500, height=400, bg="white")
canvas.pack()

grille_cliquable(canvas, L=6, H=5, taille_case=50)

fenetre.mainloop()
