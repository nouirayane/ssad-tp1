import string

ALPHABET = string.ascii_uppercase
ALPHABET_CESAR = string.ascii_uppercase + string.ascii_lowercase + string.digits + " "
ALPHABET_PLAYFAIR = string.ascii_uppercase + string.digits
ALPHABET_HILL = string.ascii_uppercase + " .,"
MOD = len(ALPHABET_HILL)


def nettoyer(texte, alphabet=ALPHABET):
    texte = texte.upper()
    resultat = ""
    for c in texte:
        if c in alphabet:
            resultat += c
    return resultat


def cesar_verifier(n):
    if n % len(ALPHABET_CESAR) == 0:
        raise ValueError("Cle faible : un decalage multiple de " + str(len(ALPHABET_CESAR)) + " ne chiffre pas le message")


def cesar_chiffrer(texte, n, sens):
    cesar_verifier(n)
    if sens == "gauche":
        n = -n
    taille = len(ALPHABET_CESAR)
    resultat = ""
    for c in texte:
        if c in ALPHABET_CESAR:
            resultat += ALPHABET_CESAR[(ALPHABET_CESAR.index(c) + n) % taille]
        else:
            resultat += c
    return resultat


def cesar_dechiffrer(texte, n, sens):
    if sens == "gauche":
        return cesar_chiffrer(texte, n, "droite")
    return cesar_chiffrer(texte, n, "gauche")


def playfair_matrice(cle):
    cle = nettoyer(cle, ALPHABET_PLAYFAIR)
    if cle == "":
        raise ValueError("La cle Playfair doit contenir des lettres ou des chiffres")
    lettres = ""
    for c in cle + ALPHABET_PLAYFAIR:
        if c not in lettres:
            lettres += c
    matrice = []
    for i in range(6):
        matrice.append(list(lettres[i * 6:i * 6 + 6]))
    return matrice


def playfair_position(matrice, lettre):
    for i in range(6):
        for j in range(6):
            if matrice[i][j] == lettre:
                return i, j


def bourrage(lettre):
    if lettre == "X":
        return "Q"
    return "X"


def playfair_paires(texte):
    texte = nettoyer(texte, ALPHABET_PLAYFAIR)
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
            resultat += matrice[l1][(c1 + d) % 6] + matrice[l2][(c2 + d) % 6]
        elif c1 == c2:
            resultat += matrice[(l1 + d) % 6][c1] + matrice[(l2 + d) % 6][c2]
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
    return playfair_traiter(playfair_paires(texte), cle, 1)


def playfair_dechiffrer(texte, cle):
    texte = nettoyer(texte, ALPHABET_PLAYFAIR)
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
    texte = nettoyer(texte, ALPHABET_HILL)
    while len(texte) % len(m) != 0:
        texte += " "
    return hill_appliquer(texte, m)


def hill_dechiffrer(texte, texte_cle):
    m = hill_cle(texte_cle)
    texte = nettoyer(texte, ALPHABET_HILL)
    if len(texte) % len(m) != 0:
        raise ValueError("La longueur du texte chiffre doit etre un multiple de " + str(len(m)))
    return hill_appliquer(texte, hill_inverse(m)).rstrip(" ")


FAILLES = {
    "Cesar": "Faille : seulement 25 cles possibles (force brute) et les espaces/majuscules restent visibles.\n"
             "Solution : alphabet etendu (majuscules, minuscules, chiffres, espace = 63 symboles),\n"
             "les espaces sont chiffres et les cles faibles (multiple de 63) sont refusees.",
    "Playfair": "Faille : I et J confondus, chiffres perdus, lettres doublees et X de bourrage dans le resultat.\n"
                "Solution : matrice 6x6 (A-Z et 0-9), lettre de bourrage X ou Q,\n"
                "et suppression du bourrage apres le dechiffrement. Cle vide refusee.",
    "Hill": "Faille : les espaces sont supprimes, une matrice non inversible empeche le dechiffrement,\n"
            "la matrice identite ne chiffre rien et une petite matrice est sensible au texte clair connu.\n"
            "Solution : alphabet de 29 symboles (A-Z, espace, point, virgule) donc les espaces sont gardes,\n"
            "modulo 29 premier, verification du determinant, refus de l'identite, matrice 3x3 possible.",
}
