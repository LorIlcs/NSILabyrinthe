import tkinter as tk

def grille(canvas, L, H, taille_case=40):
    """
    Dessine un quadrillage L x H dans un Canvas tkinter.

    - Traits intérieurs : pointillés
    - Contour extérieur : trait plein
    """
    Ox, Oy = 50, 50
    largeur = L * taille_case + Ox
    hauteur = H * taille_case + Oy

    # Traits verticaux
    for i in range(L + 1):
        x = i * taille_case + Ox
        if i == 0 or i == L:
            # Bordures
            canvas.create_line(x , Oy, x, hauteur, width=2)
        else:
            # Traits internes pointillés
            canvas.create_line(x, Oy, x, hauteur, dash=(4, 4))

    # Traits horizontaux
    for j in range(H + 1):
        y = j * taille_case + Oy
        if j == 0 or j == H:
            # Bordures
            canvas.create_line(Ox, y, largeur, y, width=2)
        else:
            # Traits internes pointillés
            canvas.create_line(Ox, y, largeur, y, dash=(4, 4))
            
            
fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, width=500, height=400, bg="white")
canvas.pack()

grille(canvas, L=8, H=6, taille_case=40)

fenetre.mainloop()




