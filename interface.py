import tkinter as tk
from tkinter import ttk, messagebox
from chiffrement import *


class FenetreChiffrement:
    def __init__(self, parent):
        self.fen = tk.Toplevel(parent)
        self.fen.title("Chiffrement / Dechiffrement")
        self.fen.geometry("620x560")

        tk.Label(self.fen, text="Entite A  ->  Entite B", font=("Arial", 14, "bold")).pack(pady=10)

        cadre = tk.Frame(self.fen)
        cadre.pack(pady=5)

        tk.Label(cadre, text="Algorithme :").grid(row=0, column=0, sticky="w", pady=4)
        self.algo = ttk.Combobox(cadre, values=["Cesar", "Playfair", "Hill"], state="readonly", width=30)
        self.algo.current(0)
        self.algo.grid(row=0, column=1, pady=4)
        self.algo.bind("<<ComboboxSelected>>", self.changer_algo)

        tk.Label(cadre, text="Cle :").grid(row=1, column=0, sticky="w", pady=4)
        self.cle = tk.Entry(cadre, width=33)
        self.cle.grid(row=1, column=1, pady=4)

        self.info = tk.Label(cadre, text="", fg="gray")
        self.info.grid(row=2, column=0, columnspan=2)

        self.label_sens = tk.Label(cadre, text="Sens :")
        self.label_sens.grid(row=3, column=0, sticky="w", pady=4)
        self.sens = ttk.Combobox(cadre, values=["Gauche -> Droite", "Droite -> Gauche"], state="readonly", width=30)
        self.sens.current(0)
        self.sens.grid(row=3, column=1, pady=4)

        tk.Label(self.fen, text="Message de A :").pack(anchor="w", padx=20)
        self.message = tk.Text(self.fen, height=4, width=70)
        self.message.pack(padx=20)

        tk.Button(self.fen, text="A chiffre et envoie a B", bg="#4a7abc", fg="white", command=self.envoyer).pack(pady=8)

        tk.Label(self.fen, text="Message chiffre recu par B :").pack(anchor="w", padx=20)
        self.chiffre = tk.Text(self.fen, height=4, width=70)
        self.chiffre.pack(padx=20)

        tk.Button(self.fen, text="B dechiffre le message", bg="#3c9a5f", fg="white", command=self.recevoir).pack(pady=8)

        tk.Label(self.fen, text="Message dechiffre par B :").pack(anchor="w", padx=20)
        self.dechiffre = tk.Text(self.fen, height=4, width=70)
        self.dechiffre.pack(padx=20)

        self.changer_algo()

    def changer_algo(self, event=None):
        a = self.algo.get()
        if a == "Cesar":
            self.info.config(text="Decalage n entre 1 et 25")
            self.label_sens.grid()
            self.sens.grid()
        elif a == "Playfair":
            self.info.config(text="Un mot cle (lettres seulement)")
            self.label_sens.grid_remove()
            self.sens.grid_remove()
        else:
            self.info.config(text="Matrice 2x2 : 4 nombres, exemple : 3 3 2 5")
            self.label_sens.grid_remove()
            self.sens.grid_remove()

    def lire_cesar(self):
        try:
            n = int(self.cle.get())
        except ValueError:
            raise ValueError("Le decalage doit etre un nombre entier")
        if n % 26 == 0:
            raise ValueError("Un decalage multiple de 26 ne chiffre pas le message")
        if self.sens.get() == "Gauche -> Droite":
            return n, "droite"
        return n, "gauche"

    def lire_playfair(self):
        if nettoyer(self.cle.get()) == "":
            raise ValueError("La cle Playfair doit contenir des lettres")
        return self.cle.get()

    def envoyer(self):
        texte = self.message.get("1.0", "end").strip()
        if nettoyer(texte) == "":
            messagebox.showwarning("Attention", "Ecrire un message", parent=self.fen)
            return
        try:
            a = self.algo.get()
            if a == "Cesar":
                n, sens = self.lire_cesar()
                res = cesar_chiffrer(texte, n, sens)
            elif a == "Playfair":
                res = playfair_chiffrer(texte, self.lire_playfair())
            else:
                res = hill_chiffrer(texte, self.cle.get())
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=self.fen)
            return
        self.chiffre.delete("1.0", "end")
        self.chiffre.insert("1.0", res)
        self.dechiffre.delete("1.0", "end")

    def recevoir(self):
        texte = self.chiffre.get("1.0", "end").strip()
        if texte == "":
            messagebox.showwarning("Attention", "Aucun message recu", parent=self.fen)
            return
        try:
            a = self.algo.get()
            if a == "Cesar":
                n, sens = self.lire_cesar()
                res = cesar_dechiffrer(texte, n, sens)
            elif a == "Playfair":
                res = playfair_dechiffrer(texte, self.lire_playfair())
            else:
                res = hill_dechiffrer(texte, self.cle.get())
        except ValueError as e:
            messagebox.showerror("Erreur", str(e), parent=self.fen)
            return
        self.dechiffre.delete("1.0", "end")
        self.dechiffre.insert("1.0", res)


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
