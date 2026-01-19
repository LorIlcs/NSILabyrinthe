import tkinter as tk


class Grille:
    def __init__(self, canvas, L, H, taille_case=40):
        self.canvas = canvas
        self.L = L
        self.H = H
        self.taille = taille_case

        # Modèle logique des arêtes
        # clé -> {"id": int, "etat": "plein|pointille", "lock": bool}
        self.aretes = {}

        self._dessiner_grille()

    # -----------------------------
    # Création des arêtes
    # -----------------------------
    def _dessiner_grille(self):

        # Arêtes verticales
        for i in range(self.L + 1):
            for j in range(self.H):
                x = i * self.taille
                y1 = j * self.taille
                y2 = y1 + self.taille
                self._creer_arete("V", i, j, x, y1, x, y2)

        # Arêtes horizontales
        for j in range(self.H + 1):
            for i in range(self.L):
                y = j * self.taille
                x1 = i * self.taille
                x2 = x1 + self.taille
                self._creer_arete("H", i, j, x1, y, x2, y)

    def _creer_arete(self, orientation, i, j, x1, y1, x2, y2):
        arete_id = self.canvas.create_line(
            x1, y1, x2, y2,
            width=2,
            dash=(),
            fill="black",
            tags=("arete",)
        )

        self.aretes[(orientation, i, j)] = {
            "id": arete_id,
            "etat": "plein",
            "lock": False
        }

        # Bind souris
        self.canvas.tag_bind(arete_id, "<Button-1>", self._clic_gauche)
        self.canvas.tag_bind(arete_id, "<Button-3>", self._clic_droit)

    # -----------------------------
    # Gestion des événements
    # -----------------------------
    def _clic_gauche(self, event):
        arete = self._arete_depuis_event()
        if arete is None or arete["lock"]:
            return

        if arete["etat"] == "plein":
            self._set_pointille(arete)
        else:
            self._set_plein(arete)

    def _clic_droit(self, event):
        arete = self._arete_depuis_event()
        if arete is None:
            return

        if arete["lock"]:
            self._deverrouiller(arete)
        else:
            self._verrouiller(arete)

    # -----------------------------
    # Outils modèle <-> vue
    # -----------------------------
    def _arete_depuis_event(self):
        courant = self.canvas.find_withtag("current")
        if not courant:
            return None

        canvas_id = courant[0]
        for data in self.aretes.values():
            if data["id"] == canvas_id:
                return data
        return None

    def _set_plein(self, arete):
        self.canvas.itemconfig(arete["id"], dash=())
        arete["etat"] = "plein"

    def _set_pointille(self, arete):
        self.canvas.itemconfig(arete["id"], dash=(4, 4))
        arete["etat"] = "pointille"

    def _verrouiller(self, arete):
        arete["lock"] = True
        self.canvas.itemconfig(
            arete["id"],
            fill="gray",
            width=3
        )

    def _deverrouiller(self, arete):
        arete["lock"] = False
        self.canvas.itemconfig(
            arete["id"],
            fill="black",
            width=2
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grille cliquable avec arêtes verrouillables")

    canvas = tk.Canvas(root, width=600, height=400, bg="white")
    canvas.pack()

    grille = Grille(canvas, L=8, H=6, taille_case=50)

    root.mainloop()
