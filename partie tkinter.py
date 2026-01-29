# ================== IMPORTS ==================

import tkinter as tk
from tkinter import PhotoImage
from time import sleep
from PIL import Image, ImageTk
import random


# ================== VARIABLES GLOBALES ==================

lignes = None
colonnes = None
auto_dep_arr = False
auto_res_laby = False

# ================== LABYRINTHE ==================

def grille_cliquable_sans_doublon(canvas, fenetre, L, H, taille_case=50, ox=50, oy=100):
    """
    Crée une grille L x H cliquable :
    - lignes pleines ou pointillées
    - possibilité de verrouiller certaines arêtes
    """
    fenetre.rowconfigure(1, weight=1)
    verrou_actif = False

    def basculer(event):
        arete = canvas.find_withtag("current")[0]
        tags = canvas.gettags(arete)

        if "Bordure" in tags or verrou_actif == True:
            return

        if "selection" in tags:
            canvas.dtag(arete, "selection")
            canvas.itemconfig(arete, dash=())
        else:
            canvas.addtag_withtag("selection", arete)
            canvas.itemconfig(arete, dash=(4, 4))

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

            arete = canvas.create_line(x, y1, x, y2, width=2, tags=tuple(tags))
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

            arete = canvas.create_line(x1, y, x2, y, width=2, tags=tuple(tags))
            canvas.tag_bind(arete, "<Button-1>", basculer)

    # --- Verrouillage ---
    def valider_selection(bouton):
        nonlocal verrou_actif
        verrou_actif = True
        
        for arete in canvas.find_withtag("selection"):
            canvas.dtag(arete, "selection")
            canvas.addtag_withtag("verrouille", arete)
            canvas.itemconfig(arete, fill="gray")
        bouton.config(state="disabled")

    bouton = tk.Button(
        fenetre,
        text="Valider les murs du labyrinthe",
        font=("", 20),
        relief="solid",
        command=lambda: valider_selection(bouton)
    )
    bouton.place(anchor="center", rely=0.95, relx=0.5, relwidth=0.25)

    def case_depart_arrive_alea(canvas, L, H, taille_case=40, ox=50, oy=50):
        bouton_depart_arrivee.config(state="disabled")
        i_dep = random.randint(0, L - 1)
        j_dep = random.randint(0, H - 1)

        x1_dep = ox + i_dep * taille_case
        y1_dep = oy + j_dep * taille_case
        x2_dep = ox + (i_dep + 1) * taille_case
        y2_dep = oy + (j_dep + 1) * taille_case

        rect_dep = canvas.create_rectangle(x1_dep, y1_dep, x2_dep, y2_dep, fill="green")

        i_ar, j_ar = i_dep, j_dep
        while i_ar == i_dep and j_ar == j_dep:
            i_ar = random.randint(0, L - 1)
            j_ar = random.randint(0, H - 1)

            x1_ar = ox + i_ar * taille_case
            y1_ar = oy + j_ar * taille_case
            x2_ar = ox + (i_ar + 1) * taille_case
            y2_ar = oy + (j_ar + 1) * taille_case

        rect_ar = canvas.create_rectangle(x1_ar, y1_ar, x2_ar, y2_ar, fill="red")
        canvas.tag_lower(rect_dep)
        canvas.tag_lower(rect_ar)


    def case_depart_arrive_manuel(canvas, L, H, taille_case=50, ox=50, oy=50):
        """
        Le joueur clique sur une case pour choisir le départ et l'arrivée.
        """
        points = {"depart": None, "arrivee": None}
        canvas.config(cursor="cross")

        def clique_case(event):
            if event.x < ox or event.y < oy:
                return

            i = (event.x - ox) // taille_case
            j = (event.y - oy) // taille_case

            if i < 0 or i >= L or j < 0 or j >= H:
                return

            x1, y1 = ox + i * taille_case, oy + j * taille_case
            x2, y2 = x1 + taille_case, y1 + taille_case

            # --- Départ ---
            if points["depart"] is None:
                points["depart"] = (i, j)
                rect_dep = canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="green",
                    tags="entree"
                )
                canvas.tag_lower(rect_dep)

            # --- Arrivée ---
            elif points["arrivee"] is None:
                if (i, j) == points["depart"]:
                    return

                points["arrivee"] = (i, j)
                rect_ar = canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="red",
                    tags="sortie"
                )
                canvas.tag_lower(rect_ar)

                canvas.unbind("<Button-1>")
                canvas.config(cursor="")
                bouton_depart_arrivee.config(state="disabled")   
        canvas.bind("<Button-1>", clique_case)


    boutton_manuel = tk.Button(
        fenetre,
        text="Placer Départ/Arrivée manuellement",
        font=("", 20),
        relief="solid",
        command = lambda: case_depart_arrive_manuel(canvas, L, H, taille_case, ox, oy)
    )
    boutton_manuel.place(rely=1, relx=1, relwidth=0.25)
    
    bouton_depart_arrivee = tk.Button(
        fenetre,
        text="Placer Départ/Arrivée",
        font=("", 20),
        relief="solid",
        command=lambda: case_depart_arrive_alea(canvas, L, H, taille_case, ox, oy)
    )
    bouton_depart_arrivee.place(rely=1, relx=1, relwidth=0.25)

    return bouton_depart_arrivee, case_depart_arrive_manuel


# ================== RESET ==================

def reset():
    """
    Plus dur que ca en a l'air, sera peut-être ajouté plus tard
    """


# ================== PARAMÈTRES ==================

def param_boutons_resol(bouton, autre_bouton):
    global auto_res_laby

    bouton.config(state="disabled")
    autre_bouton.config(state="disabled")
    bouton.config(fg="black", bg="light green")
    autre_bouton.config(fg="black", bg="red")

    if bouton.cget("text") == "Oui" and bouton.cget("bg") == "light green":
        auto_res_laby = True
    else:
        auto_res_laby = False

    print("auto_res_laby ", bouton.cget("text"))
    print("auto_res_laby ", auto_res_laby)


def param_boutons_dep_arr(bouton, autre_bouton):
    global auto_dep_arr

    bouton.config(state="disabled")
    autre_bouton.config(state="disabled")
    bouton.config(fg="black", bg="light green")
    autre_bouton.config(fg="black", bg="red")

    if bouton.cget("text") == "Aléatoirement" and bouton.cget("bg") == "light green":
        auto_dep_arr = True
    else:
        auto_dep_arr = False

    print("auto_dep_arr ", bouton.cget("text"))
    print("auto_dep_arr", auto_dep_arr)


# ================== PAGES ==================

def page_parametres():
    global lignes, colonnes

    lignes = entree_ligne.get()
    colonnes = entree_colonne.get()

    if not (lignes.isdigit() and int(lignes) <= 15 and colonnes.isdigit() and int(colonnes) <= 15):
        label_invalide = tk.Label(root, text="Entrée invalide!", fg="red", font=("", 15, "bold"))
        label_invalide.pack()
        print("Entrée invalide")
        return

    for widget in root.winfo_children():
        widget.destroy()

    frame_parent = tk.Frame(root)
    frame_parent.pack(fill="both", expand=True)

    label_titre = tk.Label(frame_parent, text="Paramètres de création", font=("", 60, "bold"))
    label_depart_arrivée = tk.Label(frame_parent, text="\nMon départ/arrivée sera sélectionné:", font=("", 30, "underline"))

    label_res_auto = tk.Label(frame_parent, text="\n\n\nRésoudre automatiquement le labyrinthe?:", font=("", 28, "underline"))

    bouton_aleatoire = tk.Button(
        frame_parent,
        text="Aléatoirement",
        font=("", 20),
        relief="solid",
        command=lambda: param_boutons_dep_arr(bouton_aleatoire, bouton_manuel)
    )

    bouton_manuel = tk.Button(
        frame_parent,
        text="Manuellement",
        font=("", 20),
        relief="solid",
        command=lambda: param_boutons_dep_arr(bouton_manuel, bouton_aleatoire)
    )

    bouton_pas_res = tk.Button(
        frame_parent,
        text="Non",
        font=("", 20),
        relief="solid",
        command=lambda: param_boutons_resol(bouton_pas_res, bouton_auto_res)
    )

    bouton_auto_res = tk.Button(
        frame_parent,
        text="Oui",
        font=("", 20),
        relief="solid",
        command=lambda: param_boutons_resol(bouton_auto_res, bouton_pas_res)
    )

    bouton_confirmer = tk.Button(
        frame_parent,
        text="Valider",
        font=("", 20),
        relief="solid",
        command=lancer_labyrinthe
    )

    label_titre.pack()
    label_depart_arrivée.pack()
    label_res_auto.pack()
    bouton_aleatoire.place(anchor="center", rely=0.23, relx=0.35, relwidth=0.25)
    bouton_manuel.place(anchor="center", rely=0.23, relx=0.65, relwidth=0.25)
    bouton_auto_res.place(anchor="center", rely=0.40, relx=0.35, relwidth=0.25)
    bouton_pas_res.place(anchor="center", rely=0.40, relx=0.65, relwidth=0.25)
    bouton_confirmer.place(anchor="center", rely=0.95, relx=0.5, relwidth=0.25)


# ================== LANCEMENT DU LABYRINTHE ==================

def lancer_labyrinthe():
    global lignes, colonnes, auto_dep_arr

    L, H = int(colonnes), int(lignes)
    taille_case = 50

    for widget in root.winfo_children():
        widget.destroy()

    frame_parent = tk.Frame(root)
    frame_parent.pack(fill="both", expand=True)

    canvas_width = L * taille_case + 100
    canvas_height = H * taille_case + 100

    label_titre_2 = tk.Label(frame_parent, text="Modifiez votre grille!", font=("", 60, "bold"))
    label_titre_2.pack()

    frame_canvas = tk.Frame(frame_parent, width=canvas_width, height=canvas_height)
    frame_canvas.pack(expand=True)
    frame_canvas.pack_propagate(False)

    canvas = tk.Canvas(frame_canvas, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(fill="both", expand=True)

    ox, oy = 50, 50

    label_manuel = tk.Label(
        frame_parent,
        text="Si le placement du départ/arrivée est manuel,\nCliquez d'abord sur la grille pour les choisir!",
        font=("", 30, "bold"),
        fg="red"
        )

    label_manuel.place(anchor="center", rely=0.2, relx=0.5)

    bouton_dep_arr, activer_mode_manuel = grille_cliquable_sans_doublon(
    canvas, root, L, H, taille_case, ox, oy)
    
    if auto_dep_arr:
        bouton_dep_arr.invoke()
    else:
        activer_mode_manuel(canvas, L, H, taille_case, ox, oy)


# ================== PROGRAMME PRINCIPAL ==================

root = tk.Tk()
root.title("Labyrinthe")
root.resizable(False, False)
root.state("zoomed")

restart_image = Image.open("image/restart.png")
restart_image_resize = restart_image.resize((50, 50))
restart_image_tk = ImageTk.PhotoImage(restart_image_resize)

label_titre = tk.Label(root, text="Générer une grille", font=("", 60, "underline", "bold"))
label_sous_titre = tk.Label(root, text="(Maximum: 15x15)", fg="blue", font=("", 30, "bold"))

label_lignes = tk.Label(root, text="Nombre de lignes", font=("", 25))
entree_ligne = tk.Entry(root, width=8, font=("", 50), justify="center")

label_colonnes = tk.Label(root, text="Nombre de colonnes", font=("", 25))
entree_colonne = tk.Entry(root, width=8, font=("", 50), justify="center")

bouton_confirmer = tk.Button(root, text="Confirmer", font=("", 20), relief="solid", command=page_parametres)

label_titre.pack(pady=20)
label_sous_titre.pack()
label_lignes.pack()
entree_ligne.pack()
label_colonnes.pack()
entree_colonne.pack()
bouton_confirmer.pack(pady=20)

root.mainloop()
