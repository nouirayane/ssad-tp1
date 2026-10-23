import tkinter as tk
from tkinter import ttk, messagebox
from chiffrement import *


class FenetreChiffrement:
    def __init__(self, parent):
        self.fen = tk.Toplevel(parent)
        self.fen.title("Chiffrement / Dechiffrement")
        self.fen.geometry("1100x700")
        self.secret_a = None
        self.secret_b = None
        self.paquet = None

        tk.Label(self.fen, text="Entite A  ->  Canal  ->  Entite B", font=("Arial", 14, "bold")).pack(pady=8)

        haut = tk.Frame(self.fen)
        haut.pack()
        tk.Label(haut, text="Algorithme :").grid(row=0, column=0, padx=4)
        self.algo = ttk.Combobox(haut, values=["Cesar", "Playfair", "Hill"], state="readonly", width=15)
        self.algo.current(0)
        self.algo.grid(row=0, column=1, padx=4)
        self.algo.bind("<<ComboboxSelected>>", self.changer_algo)
        self.label_sens = tk.Label(haut, text="Sens :")
        self.label_sens.grid(row=0, column=2, padx=4)
        self.sens = ttk.Combobox(haut, values=["Gauche -> Droite", "Droite -> Gauche"], state="readonly", width=18)
        self.sens.current(0)
        self.sens.grid(row=0, column=3, padx=4)
        tk.Button(haut, text="Echange de cle Diffie-Hellman", bg="#8a5cb8", fg="white",
                  command=self.echange_cle).grid(row=0, column=4, padx=15)

        self.failles = tk.Label(self.fen, text="", fg="#b03030", justify="left")
        self.failles.pack(pady=4)
        tk.Label(self.fen, text=PROBLEME_CLE, fg="#8a5cb8", justify="left").pack(pady=4)

        corps = tk.Frame(self.fen)
        corps.pack(pady=5)

        cadre_a = tk.LabelFrame(corps, text="Entite A", padx=8, pady=8)
        cadre_a.grid(row=0, column=0, padx=8, sticky="n")
        tk.Label(cadre_a, text="Cle secrete de A :").pack(anchor="w")
        self.cle_a = tk.Entry(cadre_a, width=40, show="*")
        self.cle_a.pack()
        self.info_a = tk.Label(cadre_a, text="", fg="gray")
        self.info_a.pack()
        tk.Label(cadre_a, text="Message :").pack(anchor="w")
        self.message = tk.Text(cadre_a, height=8, width=40)
        self.message.pack()
        tk.Button(cadre_a, text="Chiffrer et envoyer a B", bg="#4a7abc", fg="white",
                  command=self.envoyer).pack(pady=8)

        cadre_c = tk.LabelFrame(corps, text="Canal public (ce que voit un attaquant)", padx=8, pady=8)
        cadre_c.grid(row=0, column=1, padx=8, sticky="n")
        tk.Label(cadre_c, text="Valeurs Diffie-Hellman echangees :").pack(anchor="w")
        self.publics = tk.Text(cadre_c, height=5, width=40, state="disabled")
        self.publics.pack()
        tk.Label(cadre_c, text="Message chiffre transmis :").pack(anchor="w")
        self.canal = tk.Text(cadre_c, height=8, width=40, state="disabled")
        self.canal.pack()

        cadre_b = tk.LabelFrame(corps, text="Entite B", padx=8, pady=8)
        cadre_b.grid(row=0, column=2, padx=8, sticky="n")
        tk.Label(cadre_b, text="Cle secrete de B :").pack(anchor="w")
        self.cle_b = tk.Entry(cadre_b, width=40, show="*")
        self.cle_b.pack()
        self.voir = tk.BooleanVar()
        tk.Checkbutton(cadre_b, text="Afficher les cles", variable=self.voir, command=self.afficher_cles).pack()
        tk.Button(cadre_b, text="Recevoir et dechiffrer", bg="#3c9a5f", fg="white",
                  command=self.recevoir).pack(pady=8)
        tk.Label(cadre_b, text="Message recu par B :").pack(anchor="w")
        self.dechiffre = tk.Text(cadre_b, height=8, width=40)
        self.dechiffre.pack()

        self.changer_algo()

    def ecrire(self, zone, texte):
        zone.config(state="normal")
        zone.delete("1.0", "end")
        zone.insert("1.0", texte)
        zone.config(state="disabled")

    def afficher_cles(self):
        if self.voir.get():
            self.cle_a.config(show="")
            self.cle_b.config(show="")
        else:
            self.cle_a.config(show="*")
            self.cle_b.config(show="*")

    def changer_algo(self, event=None):
        a = self.algo.get()
        self.failles.config(text=FAILLES[a])
        if a == "Cesar":
            self.info_a.config(text="Decalage n (nombre entier)")
            self.label_sens.grid()
            self.sens.grid()
        elif a == "Playfair":
            self.info_a.config(text="Un mot cle")
            self.label_sens.grid_remove()
            self.sens.grid_remove()
        else:
            self.info_a.config(text="Matrice 2x2 (4 nombres) ou 3x3 (9 nombres)")
            self.label_sens.grid_remove()
            self.sens.grid_remove()
        if self.secret_a is not None:
            self.remplir_cles()

    def echange_cle(self):
        a = dh_secret()
        b = dh_secret()
        public_a = dh_public(a)
        public_b = dh_public(b)
        self.secret_a = dh_commun(public_b, a)
        self.secret_b = dh_commun(public_a, b)
        self.ecrire(self.publics, "p = 2^127 - 1    g = " + str(G) + "\n"
                    + "A envoie : " + str(public_a) + "\n"
                    + "B envoie : " + str(public_b))
        self.remplir_cles()
        messagebox.showinfo("Diffie-Hellman", "A et B ont calcule la meme cle secrete sans l'envoyer sur le canal",
                            parent=self.fen)

    def remplir_cles(self):
        algo = self.algo.get()
        self.cle_a.delete(0, "end")
        self.cle_a.insert(0, cle_depuis_secret(self.secret_a, algo))
        self.cle_b.delete(0, "end")
        self.cle_b.insert(0, cle_depuis_secret(self.secret_b, algo))

    def lire_sens(self):
        if self.sens.get() == "Gauche -> Droite":
            return "droite"
        return "gauche"

    def lire_decalage(self, cle):
        try:
            return int(cle)
        except ValueError:
            raise ValueError("Le decalage doit etre un nombre entier")

    def chiffrer(self, algo, texte, cle, sens):
        if algo == "Cesar":
            return cesar_chiffrer(texte, self.lire_decalage(cle), sens)
        if algo == "Playfair":
            return playfair_chiffrer(texte, cle)
        return hill_chiffrer(texte, cle)

    def dechiffrer(self, algo, texte, cle, sens):
        if algo == "Cesar":
            return cesar_dechiffrer(texte, self.lire_decalage(cle), sens)
        if algo == "Playfair":
            return playfair_dechiffrer(texte, cle)
        return hill_dechiffrer(texte, cle)

    def envoyer(self):
        texte = self.message.get("1.0", "end-1c").strip()
        if texte == "":
            messagebox.showwarning("Attention", "Ecrire un message", parent=self.fen)
            return
        algo = self.algo.get()
        sens = self.lire_sens()
        try:
            chiffre = self.chiffrer(algo, texte, self.cle_a.get(), sens)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=self.fen)
            return
        self.paquet = (algo, sens, chiffre)
        self.ecrire(self.canal, "[" + algo + "]\n" + chiffre)
        self.dechiffre.delete("1.0", "end")

    def recevoir(self):
        if self.paquet is None:
            messagebox.showwarning("Attention", "Aucun message recu", parent=self.fen)
            return
        algo, sens, chiffre = self.paquet
        try:
            texte = self.dechiffrer(algo, chiffre, self.cle_b.get(), sens)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=self.fen)
            return
        self.dechiffre.delete("1.0", "end")
        self.dechiffre.insert("1.0", texte)


def pas_disponible():
    messagebox.showinfo("Info", "Cette partie n'est pas encore realisee")


fenetre = tk.Tk()
fenetre.title("TP1 SSAD - Framework de chiffrement")
fenetre.geometry("400x380")

tk.Label(fenetre, text="Framework de chiffrement", font=("Arial", 16, "bold")).pack(pady=25)

tk.Button(fenetre, text="Chiffrement et Dechiffrement", width=30, height=2,
          command=lambda: FenetreChiffrement(fenetre)).pack(pady=6)
tk.Button(fenetre, text="Mots de passe", width=30, height=2, command=pas_disponible).pack(pady=6)
tk.Button(fenetre, text="Attaques", width=30, height=2, command=pas_disponible).pack(pady=6)
tk.Button(fenetre, text="Authenticite / Integrite", width=30, height=2, command=pas_disponible).pack(pady=6)

fenetre.mainloop()
