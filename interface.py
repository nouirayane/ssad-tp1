import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
from chiffrement import *

FOND = "#eef0f3"
CARTE = "#ffffff"
BORDURE = "#d5dae1"
TEXTE = "#1f2730"
GRIS = "#6b7480"
MENU = "#22303f"
MENU_TEXTE = "#b9c4d0"
MENU_SURVOL = "#2c3d50"
BLEU = "#2b67a8"
BLEU_FONCE = "#22548a"
VERT = "#2e7d4f"
ROUGE = "#a8322f"


def choisir_police():
    dispo = font.families()
    for nom in ["Segoe UI", "Inter", "Helvetica Neue", "DejaVu Sans"]:
        if nom in dispo:
            return nom
    return "TkDefaultFont"


class Carte(tk.Frame):
    def __init__(self, parent, titre, police):
        super().__init__(parent, bg=CARTE, highlightbackground=BORDURE, highlightthickness=1)
        entete = tk.Frame(self, bg=CARTE)
        entete.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(entete, text=titre, bg=CARTE, fg=TEXTE, font=(police, 11, "bold")).pack(side="left")
        tk.Frame(self, bg=BORDURE, height=1).pack(fill="x", padx=16, pady=(10, 0))
        self.corps = tk.Frame(self, bg=CARTE)
        self.corps.pack(fill="both", expand=True, padx=16, pady=12)


def zone_texte(parent, police, hauteur=5):
    cadre = tk.Frame(parent, bg=BORDURE, padx=1, pady=1)
    t = tk.Text(cadre, height=hauteur, width=10, relief="flat", wrap="word", font=(police, 11), bg="#fbfbfc",
                fg=TEXTE, insertbackground=TEXTE, padx=8, pady=6, highlightthickness=0)
    t.pack(fill="both", expand=True)
    return cadre, t


def etiquette(parent, texte, police, gris=False, gras=False):
    style = (police, 10, "bold") if gras else (police, 10)
    return tk.Label(parent, text=texte, bg=CARTE, fg=GRIS if gris else TEXTE, font=style, anchor="w", justify="left")


class Page(tk.Frame):
    titre = ""
    sous_titre = ""

    def __init__(self, parent, app):
        super().__init__(parent, bg=FOND)
        self.app = app
        self.police = app.police
        entete = tk.Frame(self, bg=FOND)
        entete.pack(fill="x", padx=28, pady=(24, 16))
        tk.Label(entete, text=self.titre, bg=FOND, fg=TEXTE, font=(self.police, 17, "bold")).pack(anchor="w")
        tk.Label(entete, text=self.sous_titre, bg=FOND, fg=GRIS, font=(self.police, 10)).pack(anchor="w", pady=(2, 0))
        self.contenu = tk.Frame(self, bg=FOND)
        self.contenu.pack(fill="both", expand=True, padx=28, pady=(0, 24))

    def carte(self, parent, titre):
        return Carte(parent, titre, self.police)


class PageAccueil(Page):
    titre = "Tableau de bord"
    sous_titre = "Sécurité des Systèmes et Audit de Données"

    def __init__(self, parent, app):
        super().__init__(parent, app)
        grille = tk.Frame(self.contenu, bg=FOND)
        grille.pack(fill="both", expand=True)
        modules = [("Chiffrement / Déchiffrement", "Partie 2",
                    "Échange d'un message entre une entité A et une entité B avec les algorithmes César, Playfair et Hill.",
                    "chiffrement"),
                   ("Mots de passe", "Partie 3",
                    "Création de mots de passe selon trois politiques et mécanismes de protection.",
                    "mots_de_passe"),
                   ("Attaques", "Partie 3",
                    "Attaque par dictionnaire et par force brute sur les trois cas, avec mesure du temps.",
                    "attaques"),
                   ("Authenticité / Intégrité", "Partie 4",
                    "Calcul et vérification d'une empreinte pour contrôler un message reçu.",
                    "integrite")]
        for i, (nom, partie, desc, cle) in enumerate(modules):
            c = tk.Frame(grille, bg=CARTE, highlightbackground=BORDURE, highlightthickness=1)
            c.grid(row=i // 2, column=i % 2, sticky="nsew", padx=(0 if i % 2 == 0 else 8, 8 if i % 2 == 0 else 0),
                   pady=(0, 16))
            tk.Frame(c, bg=BLEU, height=3).pack(fill="x")
            tk.Label(c, text=partie.upper(), bg=CARTE, fg=BLEU, font=(self.police, 9, "bold")).pack(anchor="w", padx=22, pady=(22, 0))
            tk.Label(c, text=nom, bg=CARTE, fg=TEXTE, font=(self.police, 14, "bold")).pack(anchor="w", padx=22, pady=(4, 8))
            tk.Label(c, text=desc, bg=CARTE, fg=GRIS, font=(self.police, 10), wraplength=400, justify="left").pack(anchor="w", padx=22)
            ttk.Button(c, text="Ouvrir le module", style="Principal.TButton",
                       command=lambda k=cle: self.app.afficher(k)).pack(side="bottom", anchor="w", padx=22, pady=22)
        grille.rowconfigure(0, weight=1, uniform="r")
        grille.rowconfigure(1, weight=1, uniform="r")
        grille.columnconfigure(0, weight=1, uniform="m")
        grille.columnconfigure(1, weight=1, uniform="m")


class PageChiffrement(Page):
    titre = "Chiffrement / Déchiffrement"
    sous_titre = "L'entité A chiffre un message et l'envoie à l'entité B, qui le déchiffre avec la même clé."

    def __init__(self, parent, app):
        super().__init__(parent, app)
        haut = tk.Frame(self.contenu, bg=FOND)
        haut.pack(fill="x")

        haut.columnconfigure(0, weight=3, uniform="h")
        haut.columnconfigure(1, weight=2, uniform="h")
        param = self.carte(haut, "Paramètres")
        param.grid(row=0, column=0, sticky="nsew")
        corps = param.corps

        etiquette(corps, "Algorithme", self.police, gras=True).grid(row=0, column=0, sticky="w")
        self.algo = tk.StringVar(value="Cesar")
        ligne = tk.Frame(corps, bg=CARTE)
        ligne.grid(row=0, column=1, sticky="w", padx=(20, 0))
        for nom, val in [("César", "Cesar"), ("Playfair", "Playfair"), ("Hill", "Hill")]:
            ttk.Radiobutton(ligne, text=nom, value=val, variable=self.algo,
                            command=self.changer_algo).pack(side="left", padx=(0, 18))

        etiquette(corps, "Clé", self.police, gras=True).grid(row=1, column=0, sticky="nw", pady=(14, 0))
        self.zone_cle = tk.Frame(corps, bg=CARTE)
        self.zone_cle.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=(14, 0))

        self.cadre_cesar = tk.Frame(self.zone_cle, bg=CARTE)
        etiquette(self.cadre_cesar, "Décalage n", self.police).grid(row=0, column=0, sticky="w")
        self.decalage = ttk.Spinbox(self.cadre_cesar, from_=1, to=62, width=8)
        self.decalage.set(3)
        self.decalage.grid(row=0, column=1, sticky="w", padx=10)
        etiquette(self.cadre_cesar, "Sens", self.police).grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.sens = tk.StringVar(value="droite")
        s = tk.Frame(self.cadre_cesar, bg=CARTE)
        s.grid(row=1, column=1, sticky="w", padx=10, pady=(8, 0))
        ttk.Radiobutton(s, text="Gauche → Droite", value="droite", variable=self.sens).pack(side="left", padx=(0, 14))
        ttk.Radiobutton(s, text="Droite → Gauche", value="gauche", variable=self.sens).pack(side="left")

        self.cadre_playfair = tk.Frame(self.zone_cle, bg=CARTE)
        etiquette(self.cadre_playfair, "Mot clé", self.police).grid(row=0, column=0, sticky="nw")
        self.mot_cle = tk.StringVar(value="SECURITE")
        self.mot_cle.trace_add("write", lambda *a: self.maj_matrice())
        ttk.Entry(self.cadre_playfair, textvariable=self.mot_cle, width=18).grid(row=0, column=1, sticky="nw", padx=10)
        self.matrice = tk.Frame(self.cadre_playfair, bg=BORDURE, padx=1, pady=1)
        self.matrice.grid(row=0, column=2, rowspan=2, padx=(16, 0))
        self.cases = []
        for i in range(6):
            for j in range(6):
                l = tk.Label(self.matrice, text="", width=3, bg="#f6f7f9", fg=TEXTE, font=("Courier", 10))
                l.grid(row=i, column=j, padx=1, pady=1)
                self.cases.append(l)

        self.cadre_hill = tk.Frame(self.zone_cle, bg=CARTE)
        etiquette(self.cadre_hill, "Taille", self.police).grid(row=0, column=0, sticky="w")
        self.taille = tk.IntVar(value=2)
        t = tk.Frame(self.cadre_hill, bg=CARTE)
        t.grid(row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(t, text="2 × 2", value=2, variable=self.taille, command=self.grille_hill).pack(side="left", padx=(0, 14))
        ttk.Radiobutton(t, text="3 × 3", value=3, variable=self.taille, command=self.grille_hill).pack(side="left")
        etiquette(self.cadre_hill, "Matrice", self.police).grid(row=1, column=0, sticky="nw", pady=(8, 0))
        self.cadre_matrice_hill = tk.Frame(self.cadre_hill, bg=CARTE)
        self.cadre_matrice_hill.grid(row=1, column=1, sticky="w", padx=10, pady=(8, 0))
        self.cellules = []
        self.grille_hill()

        failles = self.carte(haut, "Faille et contre-mesure")
        failles.grid(row=0, column=1, sticky="nsew", padx=(16, 0))
        self.texte_failles = tk.Label(failles.corps, text="", bg=CARTE, fg=TEXTE, font=(self.police, 10),
                                      justify="left", anchor="nw", wraplength=380)
        self.texte_failles.pack(fill="both", expand=True)
        self.texte_failles.bind("<Configure>", lambda e: self.texte_failles.config(wraplength=e.width - 4))

        bas = tk.Frame(self.contenu, bg=FOND)
        bas.pack(fill="both", expand=True, pady=(16, 0))
        bas.columnconfigure(0, weight=1, uniform="b")
        bas.columnconfigure(1, weight=1, uniform="b")
        bas.rowconfigure(0, weight=1)

        a = self.carte(bas, "Entité A  —  Émetteur")
        a.grid(row=0, column=0, sticky="nsew")
        etiquette(a.corps, "Message en clair", self.police, gris=True).pack(anchor="w")
        cadre, self.message = zone_texte(a.corps, self.police, 8)
        cadre.pack(fill="both", expand=True, pady=(4, 12))
        boutons = tk.Frame(a.corps, bg=CARTE)
        boutons.pack(fill="x")
        ttk.Button(boutons, text="Chiffrer et envoyer", style="Principal.TButton", command=self.envoyer).pack(side="left")
        ttk.Button(boutons, text="Effacer", style="Secondaire.TButton", command=self.effacer).pack(side="left", padx=8)

        b = self.carte(bas, "Entité B  —  Récepteur")
        b.grid(row=0, column=1, sticky="nsew", padx=(16, 0))
        etiquette(b.corps, "Message chiffré reçu", self.police, gris=True).pack(anchor="w")
        cadre, self.chiffre = zone_texte(b.corps, self.police, 3)
        cadre.pack(fill="both", expand=True, pady=(4, 10))
        etiquette(b.corps, "Message déchiffré", self.police, gris=True).pack(anchor="w")
        cadre, self.dechiffre = zone_texte(b.corps, self.police, 3)
        cadre.pack(fill="both", expand=True, pady=(4, 12))
        ttk.Button(b.corps, text="Déchiffrer", style="Principal.TButton", command=self.recevoir).pack(anchor="w")

        self.changer_algo()

    def grille_hill(self):
        anciennes = [c.get() for c in self.cellules]
        for w in self.cadre_matrice_hill.winfo_children():
            w.destroy()
        n = self.taille.get()
        defaut = ["3", "3", "2", "5"] if n == 2 else ["6", "24", "1", "13", "16", "10", "20", "17", "15"]
        if len(anciennes) == n * n:
            defaut = anciennes
        self.cellules = []
        for i in range(n):
            for j in range(n):
                e = ttk.Entry(self.cadre_matrice_hill, width=4, justify="center")
                e.insert(0, defaut[i * n + j])
                e.grid(row=i, column=j, padx=(0, 6), pady=(0, 6))
                self.cellules.append(e)

    def maj_matrice(self):
        try:
            m = playfair_matrice(self.mot_cle.get())
        except ValueError:
            m = [[""] * 6 for i in range(6)]
        for i in range(6):
            for j in range(6):
                self.cases[i * 6 + j].config(text=m[i][j])

    def changer_algo(self):
        for c in (self.cadre_cesar, self.cadre_playfair, self.cadre_hill):
            c.pack_forget()
        a = self.algo.get()
        if a == "Cesar":
            self.cadre_cesar.pack(anchor="w")
        elif a == "Playfair":
            self.cadre_playfair.pack(anchor="w")
            self.maj_matrice()
        else:
            self.cadre_hill.pack(anchor="w")
        self.texte_failles.config(text=FAILLES[a].replace("\n", " ").replace("Solution :", "\n\nSolution :"))

    def appliquer(self, texte, chiffrer):
        a = self.algo.get()
        if a == "Cesar":
            try:
                n = int(self.decalage.get())
            except ValueError:
                raise ValueError("Le décalage doit être un nombre entier")
            if chiffrer:
                return cesar_chiffrer(texte, n, self.sens.get())
            return cesar_dechiffrer(texte, n, self.sens.get())
        if a == "Playfair":
            if chiffrer:
                return playfair_chiffrer(texte, self.mot_cle.get())
            return playfair_dechiffrer(texte, self.mot_cle.get())
        cle = " ".join(c.get() for c in self.cellules)
        if chiffrer:
            return hill_chiffrer(texte, cle)
        return hill_dechiffrer(texte, cle)

    def ecrire(self, zone, texte):
        zone.delete("1.0", "end")
        zone.insert("1.0", texte)

    def envoyer(self):
        texte = self.message.get("1.0", "end").strip()
        if texte == "":
            messagebox.showwarning("Message vide", "Saisissez le message à envoyer.", parent=self)
            return
        try:
            res = self.appliquer(texte, True)
        except ValueError as e:
            messagebox.showerror("Clé invalide", str(e), parent=self)
            return
        self.ecrire(self.chiffre, res)
        self.dechiffre.delete("1.0", "end")
        self.app.statut("Message chiffré avec " + self.algo.get() + " et transmis à l'entité B.")

    def recevoir(self):
        texte = self.chiffre.get("1.0", "end").strip()
        if texte == "":
            messagebox.showwarning("Aucun message", "Aucun message chiffré n'a été reçu.", parent=self)
            return
        try:
            res = self.appliquer(texte, False)
        except ValueError as e:
            messagebox.showerror("Clé invalide", str(e), parent=self)
            return
        self.ecrire(self.dechiffre, res)
        self.app.statut("Message déchiffré par l'entité B.")

    def effacer(self):
        for z in (self.message, self.chiffre, self.dechiffre):
            z.delete("1.0", "end")
        self.app.statut("")


CAS = [("Cas 1", "3 caractères  ·  valeurs 0 et 1", "01", 3),
       ("Cas 2", "4 caractères  ·  valeurs 1, 2, 3, 4", "1234", 4),
       ("Cas 3", "a–z, A–Z, 0–9, +, *, …", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+*-/=@#$%&!?", 0)]


class PageMotsDePasse(Page):
    titre = "Mots de passe"
    sous_titre = "Création des mots de passe selon les trois politiques et choix des mécanismes de protection."

    def __init__(self, parent, app):
        super().__init__(parent, app)
        gauche = tk.Frame(self.contenu, bg=FOND)
        gauche.pack(side="left", fill="both", expand=True)

        politique = self.carte(gauche, "Politique")
        politique.pack(fill="x")
        self.cas = tk.IntVar(value=0)
        for i, (nom, desc, alpha, lg) in enumerate(CAS):
            ttk.Radiobutton(politique.corps, text=nom, value=i, variable=self.cas,
                            command=self.maj_info).grid(row=i, column=0, sticky="w", pady=3)
            etiquette(politique.corps, desc, self.police, gris=True).grid(row=i, column=1, sticky="w", padx=14)
        tk.Frame(politique.corps, bg=BORDURE, height=1).grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        self.info = etiquette(politique.corps, "", self.police)
        self.info.grid(row=4, column=0, columnspan=3, sticky="w")

        creation = self.carte(gauche, "Nouveau compte")
        creation.pack(fill="x", pady=(16, 0))
        c = creation.corps
        etiquette(c, "Identifiant", self.police).grid(row=0, column=0, sticky="w", pady=4)
        self.identifiant = ttk.Entry(c, width=30)
        self.identifiant.grid(row=0, column=1, sticky="w", padx=12, pady=4)
        etiquette(c, "Mot de passe", self.police).grid(row=1, column=0, sticky="w", pady=4)
        self.mdp = ttk.Entry(c, width=30, show="•")
        self.mdp.grid(row=1, column=1, sticky="w", padx=12, pady=4)
        self.voir = tk.BooleanVar()
        ttk.Checkbutton(c, text="Afficher", variable=self.voir,
                        command=lambda: self.mdp.config(show="" if self.voir.get() else "•")).grid(row=1, column=2, sticky="w")
        b = tk.Frame(c, bg=CARTE)
        b.grid(row=2, column=1, sticky="w", padx=12, pady=(10, 0))
        ttk.Button(b, text="Enregistrer", style="Principal.TButton", command=self.app.non_disponible).pack(side="left")
        ttk.Button(b, text="Tester la connexion", style="Secondaire.TButton", command=self.app.non_disponible).pack(side="left", padx=8)

        protection = self.carte(gauche, "Protection contre les attaques")
        protection.pack(fill="both", expand=True, pady=(16, 0))
        p = protection.corps
        self.options = []
        for i, texte in enumerate(["Stockage haché avec sel (SHA-256)",
                                   "Limiter le nombre de tentatives",
                                   "Délai progressif entre deux tentatives",
                                   "Verrouillage temporaire du compte"]):
            v = tk.BooleanVar(value=i < 2)
            ttk.Checkbutton(p, text=texte, variable=v).grid(row=i, column=0, sticky="w", pady=2)
            self.options.append(v)
        etiquette(p, "Tentatives max.", self.police, gris=True).grid(row=1, column=1, sticky="e", padx=(30, 6))
        s = ttk.Spinbox(p, from_=1, to=10, width=5)
        s.set(3)
        s.grid(row=1, column=2, sticky="w")

        droite = self.carte(self.contenu, "Comptes enregistrés")
        droite.pack(side="left", fill="both", expand=True, padx=(16, 0))
        self.table = ttk.Treeview(droite.corps, columns=("id", "cas", "empreinte"), show="headings", height=10)
        for col, titre, lg in [("id", "Identifiant", 110), ("cas", "Politique", 90), ("empreinte", "Empreinte stockée", 240)]:
            self.table.heading(col, text=titre, anchor="w")
            self.table.column(col, width=lg, anchor="w")
        self.table.pack(fill="both", expand=True)
        etiquette(droite.corps, "Aucun compte pour le moment.", self.police, gris=True).pack(anchor="w", pady=(8, 0))
        self.maj_info()

    def maj_info(self):
        nom, desc, alpha, lg = CAS[self.cas.get()]
        if lg:
            self.info.config(text="Alphabet : " + str(len(alpha)) + " symboles     Longueur : " + str(lg) +
                                  "     Combinaisons possibles : " + str(len(alpha) ** lg))
        else:
            self.info.config(text="Alphabet : " + str(len(alpha)) + " symboles     Longueur : libre"
                                  "     Combinaisons (8 caractères) : " + format(len(alpha) ** 8, ",").replace(",", " "))


class PageAttaques(Page):
    titre = "Attaques"
    sous_titre = "Attaque par dictionnaire et par force brute sur les trois cas, en un temps minimal."

    def __init__(self, parent, app):
        super().__init__(parent, app)
        haut = tk.Frame(self.contenu, bg=FOND)
        haut.pack(fill="x")

        conf = self.carte(haut, "Configuration")
        conf.pack(side="left", fill="both", expand=True)
        c = conf.corps
        etiquette(c, "Cible", self.police).grid(row=0, column=0, sticky="w", pady=4)
        self.cible = ttk.Combobox(c, values=[n + "  —  " + d for n, d, a, l in CAS], state="readonly", width=40)
        self.cible.current(0)
        self.cible.grid(row=0, column=1, columnspan=2, sticky="w", padx=12, pady=4)
        etiquette(c, "Compte", self.police).grid(row=1, column=0, sticky="w", pady=4)
        ttk.Combobox(c, values=[], state="readonly", width=40).grid(row=1, column=1, columnspan=2, sticky="w", padx=12, pady=4)
        etiquette(c, "Méthode", self.police).grid(row=2, column=0, sticky="w", pady=4)
        self.methode = tk.StringVar(value="force")
        m = tk.Frame(c, bg=CARTE)
        m.grid(row=2, column=1, columnspan=2, sticky="w", padx=12, pady=4)
        ttk.Radiobutton(m, text="Force brute", value="force", variable=self.methode).pack(side="left", padx=(0, 18))
        ttk.Radiobutton(m, text="Dictionnaire", value="dico", variable=self.methode).pack(side="left")
        etiquette(c, "Dictionnaire", self.police).grid(row=3, column=0, sticky="w", pady=4)
        self.fichier = ttk.Entry(c, width=32)
        self.fichier.grid(row=3, column=1, sticky="w", padx=12, pady=4)
        ttk.Button(c, text="Parcourir…", style="Secondaire.TButton", command=self.parcourir).grid(row=3, column=2, sticky="w")

        suivi = self.carte(haut, "Exécution")
        suivi.pack(side="left", fill="both", padx=(16, 0))
        s = suivi.corps
        b = tk.Frame(s, bg=CARTE)
        b.pack(anchor="w")
        ttk.Button(b, text="Lancer l'attaque", style="Principal.TButton", command=self.app.non_disponible).pack(side="left")
        ttk.Button(b, text="Arrêter", style="Secondaire.TButton", command=self.app.non_disponible).pack(side="left", padx=8)
        self.barre = ttk.Progressbar(s, length=320, mode="determinate")
        self.barre.pack(anchor="w", pady=(16, 8))
        compteurs = tk.Frame(s, bg=CARTE)
        compteurs.pack(anchor="w", fill="x")
        for i, (titre, val) in enumerate([("Tentatives", "0"), ("Temps écoulé", "0.000 s"), ("Résultat", "—")]):
            etiquette(compteurs, titre, self.police, gris=True).grid(row=0, column=i, sticky="w", padx=(0, 28))
            tk.Label(compteurs, text=val, bg=CARTE, fg=TEXTE, font=(self.police, 14, "bold")).grid(row=1, column=i, sticky="w")

        bas = tk.Frame(self.contenu, bg=FOND)
        bas.pack(fill="both", expand=True, pady=(16, 0))
        bas.columnconfigure(0, weight=1, uniform="b")
        bas.columnconfigure(1, weight=1, uniform="b")
        bas.rowconfigure(0, weight=1)
        res = self.carte(bas, "Historique des attaques")
        res.grid(row=0, column=0, sticky="nsew")
        self.table = ttk.Treeview(res.corps, columns=("cas", "methode", "tentatives", "temps", "trouve"),
                                  show="headings", height=8)
        for col, titre, lg in [("cas", "Cas", 55), ("methode", "Méthode", 95), ("tentatives", "Tentatives", 80),
                               ("temps", "Temps (s)", 75), ("trouve", "Trouvé", 90)]:
            self.table.heading(col, text=titre, anchor="w")
            self.table.column(col, width=lg, anchor="w")
        self.table.pack(fill="both", expand=True)

        journal = self.carte(bas, "Journal")
        journal.grid(row=0, column=1, sticky="nsew", padx=(16, 0))
        cadre, self.journal = zone_texte(journal.corps, self.police, 8)
        self.journal.config(font=("Courier", 10), fg=GRIS)
        self.journal.insert("1.0", "En attente du lancement d'une attaque.")
        self.journal.config(state="disabled")
        cadre.pack(fill="both", expand=True)

    def parcourir(self):
        nom = filedialog.askopenfilename(parent=self, title="Choisir un dictionnaire",
                                         filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
        if nom:
            self.fichier.delete(0, "end")
            self.fichier.insert(0, nom)


class PageIntegrite(Page):
    titre = "Authenticité / Intégrité"
    sous_titre = "L'entité A joint une empreinte au message ; l'entité B la recalcule pour contrôler le message reçu."

    def __init__(self, parent, app):
        super().__init__(parent, app)
        obj = self.carte(self.contenu, "Objectif")
        obj.pack(fill="x")
        o = obj.corps
        self.objectif = tk.StringVar(value="integrite")
        ttk.Radiobutton(o, text="Intégrité  —  empreinte SHA-256", value="integrite", variable=self.objectif,
                        command=self.maj_cle).grid(row=0, column=0, sticky="w", padx=(0, 30))
        ttk.Radiobutton(o, text="Authenticité  —  HMAC-SHA256 avec clé partagée", value="authenticite",
                        variable=self.objectif, command=self.maj_cle).grid(row=0, column=1, sticky="w")
        etiquette(o, "Clé partagée", self.police).grid(row=1, column=0, sticky="w", pady=(12, 0))
        self.cle = ttk.Entry(o, width=40, show="•")
        self.cle.grid(row=1, column=1, sticky="w", pady=(12, 0))

        bas = tk.Frame(self.contenu, bg=FOND)
        bas.pack(fill="both", expand=True, pady=(16, 0))
        bas.columnconfigure(0, weight=1, uniform="b")
        bas.columnconfigure(1, weight=1, uniform="b")
        bas.rowconfigure(0, weight=1)

        a = self.carte(bas, "Entité A  —  Émetteur")
        a.grid(row=0, column=0, sticky="nsew")
        etiquette(a.corps, "Message", self.police, gris=True).pack(anchor="w")
        cadre, self.message = zone_texte(a.corps, self.police, 7)
        cadre.pack(fill="both", expand=True, pady=(4, 10))
        etiquette(a.corps, "Empreinte générée", self.police, gris=True).pack(anchor="w")
        self.empreinte = ttk.Entry(a.corps, state="readonly", font=("Courier", 10))
        self.empreinte.pack(fill="x", pady=(4, 12))
        ttk.Button(a.corps, text="Générer et envoyer", style="Principal.TButton",
                   command=self.app.non_disponible).pack(anchor="w")

        b = self.carte(bas, "Entité B  —  Récepteur")
        b.grid(row=0, column=1, sticky="nsew", padx=(16, 0))
        etiquette(b.corps, "Message reçu", self.police, gris=True).pack(anchor="w")
        cadre, self.recu = zone_texte(b.corps, self.police, 7)
        cadre.pack(fill="both", expand=True, pady=(4, 10))
        etiquette(b.corps, "Empreinte reçue", self.police, gris=True).pack(anchor="w")
        self.empreinte_recue = ttk.Entry(b.corps, font=("Courier", 10))
        self.empreinte_recue.pack(fill="x", pady=(4, 12))
        ligne = tk.Frame(b.corps, bg=CARTE)
        ligne.pack(fill="x")
        ttk.Button(ligne, text="Vérifier", style="Principal.TButton", command=self.app.non_disponible).pack(side="left")
        self.verdict = tk.Label(ligne, text="En attente de vérification", bg="#f1f2f4", fg=GRIS,
                                font=(self.police, 10), padx=10, pady=4)
        self.verdict.pack(side="left", padx=12)
        self.maj_cle()

    def maj_cle(self):
        self.cle.config(state="normal" if self.objectif.get() == "authenticite" else "disabled")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SSAD")
        self.geometry("1280x820")
        self.minsize(1180, 760)
        self.configure(bg=FOND)
        self.police = choisir_police()
        self.styles()

        menu = tk.Frame(self, bg=MENU, width=250)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)
        tk.Label(menu, text="SSAD", bg=MENU, fg="white", font=(self.police, 18, "bold")).pack(anchor="w", padx=22, pady=(24, 22))
        tk.Frame(menu, bg="#34465a", height=1).pack(fill="x", padx=22, pady=(0, 14))

        self.boutons = {}
        for cle, texte in [("accueil", "Tableau de bord"),
                           ("chiffrement", "Chiffrement / Déchiffrement"),
                           ("mots_de_passe", "Mots de passe"),
                           ("attaques", "Attaques"),
                           ("integrite", "Authenticité / Intégrité")]:
            ligne = tk.Frame(menu, bg=MENU)
            ligne.pack(fill="x")
            repere = tk.Frame(ligne, bg=MENU, width=3)
            repere.pack(side="left", fill="y")
            b = tk.Label(ligne, text=texte, bg=MENU, fg=MENU_TEXTE, font=(self.police, 11), anchor="w",
                         padx=19, pady=11, cursor="hand2")
            b.pack(side="left", fill="x", expand=True)
            b.bind("<Button-1>", lambda e, k=cle: self.afficher(k))
            b.bind("<Enter>", lambda e, k=cle: self.survol(k, True))
            b.bind("<Leave>", lambda e, k=cle: self.survol(k, False))
            self.boutons[cle] = (repere, b)


        droite = tk.Frame(self, bg=FOND)
        droite.pack(side="left", fill="both", expand=True)
        barre = tk.Frame(droite, bg=CARTE, highlightbackground=BORDURE, highlightthickness=1)
        barre.pack(side="bottom", fill="x")
        self.texte_statut = tk.Label(barre, text="", bg=CARTE, fg=GRIS, font=(self.police, 9), anchor="w")
        self.texte_statut.pack(side="left", padx=12, pady=4)

        zone = tk.Frame(droite, bg=FOND)
        zone.pack(fill="both", expand=True)
        self.pages = {"accueil": PageAccueil(zone, self),
                      "chiffrement": PageChiffrement(zone, self),
                      "mots_de_passe": PageMotsDePasse(zone, self),
                      "attaques": PageAttaques(zone, self),
                      "integrite": PageIntegrite(zone, self)}
        for p in self.pages.values():
            p.place(relwidth=1, relheight=1)
        self.actuelle = None
        self.afficher("accueil")

    def styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        p = self.police
        s.configure(".", font=(p, 10), background=CARTE, foreground=TEXTE)
        s.configure("TRadiobutton", background=CARTE, font=(p, 10))
        s.configure("TCheckbutton", background=CARTE, font=(p, 10))
        s.map("TRadiobutton", background=[("active", CARTE)])
        s.map("TCheckbutton", background=[("active", CARTE)])
        s.configure("TEntry", fieldbackground="#fbfbfc", bordercolor=BORDURE, lightcolor=BORDURE, padding=4)
        s.map("TEntry", bordercolor=[("focus", BLEU)], lightcolor=[("focus", BLEU)])
        s.configure("TSpinbox", fieldbackground="#fbfbfc", bordercolor=BORDURE, lightcolor=BORDURE, padding=3,
                    arrowsize=11)
        s.configure("TCombobox", fieldbackground="#fbfbfc", bordercolor=BORDURE, lightcolor=BORDURE, padding=3)
        s.map("TCombobox", fieldbackground=[("readonly", "#fbfbfc")])
        s.configure("Principal.TButton", background=BLEU, foreground="white", bordercolor=BLEU_FONCE,
                    lightcolor=BLEU, darkcolor=BLEU_FONCE, font=(p, 10, "bold"), padding=(16, 7))
        s.map("Principal.TButton", background=[("pressed", BLEU_FONCE), ("active", BLEU_FONCE)])
        s.configure("Secondaire.TButton", background="#f4f5f7", foreground=TEXTE, bordercolor=BORDURE,
                    lightcolor="#f4f5f7", darkcolor=BORDURE, padding=(14, 7))
        s.map("Secondaire.TButton", background=[("pressed", "#e3e6ea"), ("active", "#e9ebee")])
        s.configure("Treeview", background=CARTE, fieldbackground=CARTE, rowheight=28, bordercolor=BORDURE,
                    font=(p, 10))
        s.configure("Treeview.Heading", background="#f4f5f7", foreground=GRIS, font=(p, 10, "bold"),
                    bordercolor=BORDURE, relief="flat", padding=(6, 5))
        s.map("Treeview.Heading", background=[("active", "#eceef1")])
        s.configure("Horizontal.TProgressbar", background=BLEU, troughcolor="#e6e9ed", bordercolor=BORDURE,
                    lightcolor=BLEU, darkcolor=BLEU, thickness=8)

    def survol(self, cle, dedans):
        if cle == self.actuelle:
            return
        self.boutons[cle][1].config(bg=MENU_SURVOL if dedans else MENU)

    def afficher(self, cle):
        self.actuelle = cle
        for k, (repere, b) in self.boutons.items():
            if k == cle:
                repere.config(bg="#5d9be0")
                b.config(bg=MENU_SURVOL, fg="white")
            else:
                repere.config(bg=MENU)
                b.config(bg=MENU, fg=MENU_TEXTE)
        self.pages[cle].tkraise()
        self.statut("")

    def statut(self, texte):
        self.texte_statut.config(text=texte)

    def non_disponible(self):
        self.statut("Cette fonctionnalité sera ajoutée dans une prochaine version.")
        messagebox.showinfo("Non disponible", "Cette fonctionnalité n'est pas encore réalisée.", parent=self)


if __name__ == "__main__":
    Application().mainloop()
