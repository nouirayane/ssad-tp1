import string
import random
import secrets
import unicodedata

SYMBOLES = string.ascii_uppercase + string.ascii_lowercase + string.digits + " .,;:!?'-()\"/@#%&*+"
ALPHABET_HILL = SYMBOLES + "=_"
MOD = len(ALPHABET_HILL)


def enlever_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    return "".join(c for c in texte if unicodedata.category(c) != "Mn")


def nettoyer(texte, alphabet):
    texte = enlever_accents(texte).replace("\n", " ")
    for c in texte:
        if c not in alphabet:
            raise ValueError("Caractere non supporte : " + c)
    return texte


def cesar_verifier(n):
    if n % len(SYMBOLES) == 0:
        raise ValueError("Cle faible : un decalage multiple de " + str(len(SYMBOLES)) + " ne chiffre pas le message")


def cesar_chiffrer(texte, n, sens):
    cesar_verifier(n)
    if sens == "gauche":
        n = -n
    texte = nettoyer(texte, SYMBOLES)
    resultat = ""
    for c in texte:
        resultat += SYMBOLES[(SYMBOLES.index(c) + n) % len(SYMBOLES)]
    return resultat


def cesar_dechiffrer(texte, n, sens):
    if sens == "gauche":
        return cesar_chiffrer(texte, n, "droite")
    return cesar_chiffrer(texte, n, "gauche")


def playfair_matrice(cle):
    cle = nettoyer(cle, SYMBOLES)
    if cle.strip() == "":
        raise ValueError("La cle Playfair ne doit pas etre vide")
    lettres = ""
    for c in cle + SYMBOLES:
        if c not in lettres:
            lettres += c
    matrice = []
    for i in range(9):
        matrice.append(list(lettres[i * 9:i * 9 + 9]))
    return matrice


def playfair_position(matrice, lettre):
    for i in range(9):
        for j in range(9):
            if matrice[i][j] == lettre:
                return i, j


def bourrage(lettre):
    if lettre == "X":
        return "Q"
    return "X"


def playfair_paires(texte):
    paires = []
    i = 0
    while i < len(texte):
        a = texte[i]
        if i + 1 < len(texte):
            b = texte[i + 1]
        else:
            b = ""
        if b == "" or a == b:
            paires.append(a + bourrage(a))
            i += 1
        else:
            paires.append(a + b)
            i += 2
    return paires


def playfair_traiter(paires, cle, d):
    matrice = playfair_matrice(cle)
    resultat = ""
    for p in paires:
        l1, c1 = playfair_position(matrice, p[0])
        l2, c2 = playfair_position(matrice, p[1])
        if l1 == l2:
            resultat += matrice[l1][(c1 + d) % 9] + matrice[l2][(c2 + d) % 9]
        elif c1 == c2:
            resultat += matrice[(l1 + d) % 9][c1] + matrice[(l2 + d) % 9][c2]
        else:
            resultat += matrice[l1][c2] + matrice[l2][c1]
    return resultat


def playfair_enlever_bourrage(texte):
    resultat = ""
    for i in range(len(texte)):
        c = texte[i]
        if i % 2 == 1 and c == bourrage(texte[i - 1]):
            if i == len(texte) - 1 or texte[i - 1] == texte[i + 1]:
                continue
        resultat += c
    return resultat


def playfair_chiffrer(texte, cle):
    texte = nettoyer(texte, SYMBOLES)
    return playfair_traiter(playfair_paires(texte), cle, 1)


def playfair_dechiffrer(texte, cle):
    texte = nettoyer(texte, SYMBOLES)
    if len(texte) % 2 != 0:
        raise ValueError("Le texte chiffre doit avoir un nombre pair de caracteres")
    paires = [texte[i:i + 2] for i in range(0, len(texte), 2)]
    return playfair_enlever_bourrage(playfair_traiter(paires, cle, -1))


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def inverse_modulo(a, mod):
    for x in range(1, mod):
        if (a * x) % mod == 1:
            return x
    return None


def sous_matrice(m, ligne, colonne):
    return [[m[i][j] for j in range(len(m)) if j != colonne] for i in range(len(m)) if i != ligne]


def determinant(m):
    if len(m) == 1:
        return m[0][0]
    det = 0
    for j in range(len(m)):
        det += (-1) ** j * m[0][j] * determinant(sous_matrice(m, 0, j))
    return det


def hill_cle(texte_cle):
    try:
        nombres = [int(x) % MOD for x in texte_cle.replace(",", " ").split()]
    except ValueError:
        raise ValueError("La cle de Hill doit contenir uniquement des nombres")
    if len(nombres) == 4:
        n = 2
    elif len(nombres) == 9:
        n = 3
    else:
        raise ValueError("La cle de Hill doit contenir 4 nombres (2x2) ou 9 nombres (3x3)")
    m = [nombres[i * n:i * n + n] for i in range(n)]
    det = determinant(m) % MOD
    if pgcd(det, MOD) != 1:
        raise ValueError("Cle non valide : le determinant (" + str(det) + ") n'est pas inversible modulo " + str(MOD))
    identite = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    if m == identite:
        raise ValueError("Cle faible : la matrice identite ne chiffre pas le message")
    return m


def hill_inverse(m):
    n = len(m)
    inv = inverse_modulo(determinant(m) % MOD, MOD)
    if n == 2:
        return [[(m[1][1] * inv) % MOD, (-m[0][1] * inv) % MOD],
                [(-m[1][0] * inv) % MOD, (m[0][0] * inv) % MOD]]
    resultat = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            cofacteur = (-1) ** (i + j) * determinant(sous_matrice(m, i, j))
            resultat[j][i] = (cofacteur * inv) % MOD
    return resultat


def hill_appliquer(texte, m):
    n = len(m)
    resultat = ""
    for i in range(0, len(texte), n):
        bloc = [ALPHABET_HILL.index(c) for c in texte[i:i + n]]
        for ligne in m:
            somme = 0
            for k in range(n):
                somme += ligne[k] * bloc[k]
            resultat += ALPHABET_HILL[somme % MOD]
    return resultat


def hill_chiffrer(texte, texte_cle):
    m = hill_cle(texte_cle)
    texte = nettoyer(texte, SYMBOLES)
    while len(texte) % len(m) != 0:
        texte += " "
    return hill_appliquer(texte, m)


def hill_dechiffrer(texte, texte_cle):
    m = hill_cle(texte_cle)
    texte = nettoyer(texte, ALPHABET_HILL)
    if len(texte) % len(m) != 0:
        raise ValueError("La longueur du texte chiffre doit etre un multiple de " + str(len(m)))
    return hill_appliquer(texte, hill_inverse(m)).rstrip(" ")


P = 2 ** 127 - 1
G = 5


def dh_secret():
    return secrets.randbelow(P - 3) + 2


def dh_public(secret):
    return pow(G, secret, P)


def dh_commun(public_autre, secret):
    return pow(public_autre, secret, P)


def cle_depuis_secret(s, algo):
    if algo == "Cesar":
        return str(s % (len(SYMBOLES) - 1) + 1)
    if algo == "Playfair":
        mot = ""
        while len(mot) < 12:
            mot += SYMBOLES[s % len(SYMBOLES)]
            s //= len(SYMBOLES)
        return mot
    r = random.Random(s)
    while True:
        nombres = [r.randrange(MOD) for i in range(9)]
        try:
            hill_cle(" ".join(str(x) for x in nombres))
            return " ".join(str(x) for x in nombres)
        except ValueError:
            pass


FAILLES = {
    "Cesar": "Faille : peu de cles possibles (force brute) et les caracteres non chiffres restent visibles.\n"
             "Solution : alphabet de " + str(len(SYMBOLES)) + " symboles (majuscules, minuscules, chiffres, espace, ponctuation),\n"
             "tout le message est chiffre et les cles faibles sont refusees.",
    "Playfair": "Faille : I et J confondus, espaces, chiffres et ponctuation perdus, lettres doublees.\n"
                "Solution : matrice 9x9 (" + str(len(SYMBOLES)) + " symboles), lettre de bourrage X ou Q\n"
                "supprimee apres le dechiffrement. Cle vide refusee.",
    "Hill": "Faille : caracteres supprimes, matrice non inversible, matrice identite, attaque par texte clair connu.\n"
            "Solution : alphabet de " + str(MOD) + " symboles (modulo premier), verification du determinant,\n"
            "refus de l'identite, matrice 3x3 possible.",
}

PROBLEME_CLE = ("Probleme de la cle : si A envoie la cle a B sur le meme canal que le message, un attaquant\n"
                "la recupere et dechiffre tout. Solution : echange de cle Diffie-Hellman. A et B envoient\n"
                "seulement des valeurs publiques, chacun calcule le meme secret, la cle ne passe jamais sur le canal.")
