import tkinter as tk
import random 

def grille_cliquable_sans_doublon(canvas, L, H, taille_case=40, ox=50, oy=100):
    """
    Quadrillage L x H :
    - aucune arête dupliquée
    - chaque arête est cliquable
    - clic : plein <-> pointillé
    """

    def basculer(event):
        arete = canvas.find_withtag("current")[0]
        tags = canvas.gettags(arete)
        
        if "Bordure" in tags or "verrouille" in tags:
            return

        if "selection" in tags:
            canvas.dtag("selection", arete)
            canvas.itemconfig(arete, dash=())
        else:
            canvas.addtag_withtag("selection", arete)
            canvas.itemconfig(arete, dash = (4,4))
        
        if "pointille" in tags:
            canvas.itemconfig(arete, dash=())
            canvas.dtag(arete, "pointille")
            canvas.addtag_withtag("plein", arete)
        else:
            canvas.itemconfig(arete, dash=(4, 4))
            canvas.dtag(arete, "plein")
            canvas.addtag_withtag("pointille", arete)

    # --- Arêtes verticales ---
    for i in range(L + 1):
        for j in range(H):
            x = i * taille_case + ox
            y1 = j * taille_case + oy
            y2 = y1 + taille_case

            tags = ["arete", "plein"]
            if i == 0 or i == L:
                tags.append("Bordure")
                
            arete = canvas.create_line(
                x, y1, x, y2,
                width=2,
                dash=(),
                tags= tuple(tags)
            )
            canvas.tag_bind(arete, "<Button-1>", basculer)
           

    # --- Arêtes horizontales ---
    for j in range(H + 1):
        for i in range(L):
            y = j * taille_case + oy
            x1 = i * taille_case + ox
            x2 = x1 + taille_case

            tags = ["arete", "plein"]
            if j == 0 or j == H:
                tags.append("Bordure")

            arete = canvas.create_line(
                x1, y, x2, y,
                width=2,
                dash=(),
                tags=tuple(tags)
            )
            canvas.tag_bind(arete, "<Button-1>", basculer)



    # --- Verrouillage des murs---

    def valider_selection(canvas):
        for arete in canvas.find_withtag("selection"):
            canvas.dtag(arete, "selection")
            canvas.addtag_withtag("verrouille", arete)
            canvas.itemconfig(arete, fill="gray")


   #---Bouton verrouillage des murs du labyrinth---
            

    bouton = tk.Button(fenetre, text = "Valider les murs du Labyrinth", command=lambda: valider_selection(canvas))
    bouton.pack()

    

   #---selection point de départ et d'arriver aléatoirs---

    def case_depart_arrive_alea(canvas, L, H, taille_case=40, ox=50, oy=100):
        
        i_dep = random.randint(0, L-1)
        j_dep = random.randint(0, H-1)

        x1_dep = ox + i_dep * taille_case
        y1_dep = oy + j_dep * taille_case
        x2_dep = ox + (i_dep + 1) * taille_case
        y2_dep = oy + (j_dep +1) * taille_case

        rect_dep = canvas.create_rectangle(x1_dep,y1_dep,x2_dep,y2_dep, fill ="green")

        i_ar, j_ar = i_dep, j_dep
        while i_ar == i_dep and j_ar == j_dep:
            i_ar = random.randint(0, L-1)
            j_ar = random.randint(0, H-1)
       
            x1_ar = ox + i_ar* taille_case
            y1_ar= oy + j_ar * taille_case
            x2_ar =  ox + (i_ar + 1)* taille_case
            y2_ar =  oy + (j_ar +1) * taille_case

        rect_ar = canvas.create_rectangle(x1_ar,y1_ar,x2_ar,y2_ar, fill ="red")
        canvas.tag_lower(rect_dep)
        canvas.tag_lower(rect_ar)

    btn_cadre = tk.Frame(fenetre)
    btn_cadre.pack(pady=10)
    
    tk.Button(btn_cadre, text="Placer Départ/Arrivée", command = lambda:case_depart_arrive_alea(canvas, L=6, H=5, taille_case=50)).pack(side="left", padx=5)




            
        
        

    



fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, width=500, height=400, bg="white")
canvas.pack()

grille_cliquable_sans_doublon(canvas, L=6, H=5, taille_case=50)

fenetre.mainloop()
