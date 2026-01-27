import tkinter as tk
from tkinter import PhotoImage
from time import sleep
from PIL import Image, ImageTk
import random 

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
    bouton.place(anchor="center", rely=0.95, relx=0.35, relwidth = 0.25)

    
    def case_depart_arrive_alea(canvas, L, H, taille_case=40, ox=50, oy=50):
        bouton_depart_arrivee.config(state="disabled")
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
    
    bouton_depart_arrivee = tk.Button(fenetre, text="Placer Départ/Arrivée",
              font=("", 20), relief="solid",
              command = lambda:case_depart_arrive_alea(canvas, L=L, H=H, taille_case=taille_case, ox=ox, oy=oy)
              )
    bouton_depart_arrivee.place(anchor="center", rely=0.95, relx=0.65, relwidth = 0.25)


# ================== RESTART ==================

def reset():
    """
    Plus dur que ca en a l'air, sera peux etre ajouté plus tard
    """

# ================== ECRAN DE SELECTION ==================

def lancer_labyrinthe():
    lignes = entree_ligne.get()
    colonnes = entree_colonne.get()

    if not (lignes.isdigit() and int(lignes) <= 15 and colonnes.isdigit() and int(colonnes) <= 15):
        label_invalide = tk.Label(root, text="Entrée invalide!", fg="red", font=("", 15, "bold"))
        label_invalide.pack()
        
        print("Entrée invalide")
        return

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

    bouton_reset = tk.Button(frame_parent, image=restart_image_tk, width=restart_image_width, height=restart_image_height, relief="solid",
                         command=reset)
    #bouton_reset.place(relx=0.04, rely=0.01, anchor="ne")
    
    ox, oy = 50, 50
    
    grille_cliquable_sans_doublon(canvas, root, L, H, taille_case=taille_case, ox=ox, oy=oy)


# ================== PROGRAMME PRINCIPAL ==================

root = tk.Tk()
root.title("Labyrinthe")
root.resizable(False, False) 
root.state("zoomed")

restart_image = Image.open("image/restart.png")
restart_image_width = 50
restart_image_height = 50
restart_image_resize = restart_image.resize((restart_image_width, restart_image_height))
restart_image_tk = ImageTk.PhotoImage(restart_image_resize)


bouton_reset = tk.Button(root, image=restart_image_tk, width=restart_image_width, height=restart_image_height, relief="solid",
                         command=reset)
#bouton_reset.place(relx=0.04, rely=0.01, anchor="ne")

label_titre = tk.Label(root, text="Générer une grille", font=("", 60, "underline", "bold"))
label_sous_titre = tk.Label(root, text="(Maximum: 15x15)", fg="blue", font=("", 30, "bold"))
label_sous_titre_2 = tk.Label(root, text=" ", font=("", 10))

label_lignes = tk.Label(root, text="Nombre de lignes", font=("", 25))
entree_ligne = tk.Entry(root, borderwidth=3, relief="solid", highlightthickness=5, width=8, font=("", 50), justify="center")

label_colonnes = tk.Label(root, text="Nombre de colonnes", font=("", 25))
entree_colonne = tk.Entry(root, borderwidth=3, relief="solid", highlightthickness=5, width=8, font=("", 50), justify="center")

bouton_confirmer = tk.Button(
    root,   
    text="Confirmer",
    font=("", 20),
    relief="solid",
    command=lancer_labyrinthe
)

label_titre.pack(pady=20)
label_sous_titre.pack()
label_sous_titre_2.pack()
label_lignes.pack()
entree_ligne.pack()
label_colonnes.pack()
entree_colonne.pack()
bouton_confirmer.pack(pady=20)

root.mainloop()
