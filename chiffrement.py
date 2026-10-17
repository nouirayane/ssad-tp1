ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def nettoyer(texte):
    texte = texte.upper()
    resultat = ""
    for c in texte:
        if c in ALPHABET:
            resultat += c
    return resultat


def cesar_chiffrer(texte, n, sens):
    if sens == "gauche":
        n = -n
    resultat = ""
    for c in texte.upper():
        if c in ALPHABET:
            resultat += ALPHABET[(ALPHABET.index(c) + n) % 26]
        else:
            resultat += c
    return resultat


def cesar_dechiffrer(texte, n, sens):
    if sens == "gauche":
        return cesar_chiffrer(texte, n, "droite")
    return cesar_chiffrer(texte, n, "gauche")


def playfair_matrice(cle):
    cle = nettoyer(cle).replace("J", "I")
    lettres = ""
    for c in cle + ALPHABET:
        if c == "J":
            continue
        if c not in lettres:
            lettres += c
    matrice = []
    for i in range(5):
        matrice.append(list(lettres[i * 5:i * 5 + 5]))
    return matrice


def playfair_position(matrice, lettre):
    for i in range(5):
        for j in range(5):
            if matrice[i][j] == lettre:
                return i, j


def playfair_paires(texte):
    texte = nettoyer(texte).replace("J", "I")
    paires = []
    i = 0
    while i < len(texte):
        a = texte[i]
        if i + 1 < len(texte):
            b = texte[i + 1]
        else:
            b = ""
        if b == "" or a == b:
            if a == "X":
                paires.append(a + "Q")
            else:
                paires.append(a + "X")
            i += 1
        else:
            paires.append(a + b)
            i += 2
    return paires


def playfair_traiter(texte, cle, d):
    matrice = playfair_matrice(cle)
    if d == 1:
        paires = playfair_paires(texte)
    else:
        texte = nettoyer(texte)
        paires = [texte[i:i + 2] for i in range(0, len(texte), 2)]
    resultat = ""
    for p in paires:
        l1, c1 = playfair_position(matrice, p[0])
        l2, c2 = playfair_position(matrice, p[1])
        if l1 == l2:
            resultat += matrice[l1][(c1 + d) % 5] + matrice[l2][(c2 + d) % 5]
        elif c1 == c2:
            resultat += matrice[(l1 + d) % 5][c1] + matrice[(l2 + d) % 5][c2]
        else:
            resultat += matrice[l1][c2] + matrice[l2][c1]
    return resultat


def playfair_chiffrer(texte, cle):
    return playfair_traiter(texte, cle, 1)


def playfair_dechiffrer(texte, cle):
    if len(nettoyer(texte)) % 2 != 0:
        raise ValueError("Le texte chiffre doit avoir un nombre pair de lettres")
    return playfair_traiter(texte, cle, -1)


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def inverse_mod26(a):
    for x in range(1, 26):
        if (a * x) % 26 == 1:
            return x
    return None


def hill_cle(texte_cle):
    nombres = [int(x) for x in texte_cle.replace(",", " ").split()]
    if len(nombres) != 4:
        raise ValueError("La cle de Hill doit contenir 4 nombres (matrice 2x2)")
    a, b, c, d = [x % 26 for x in nombres]
    det = (a * d - b * c) % 26
    if pgcd(det, 26) != 1:
        raise ValueError("Cle non valide : le determinant (" + str(det) + ") n'est pas inversible modulo 26")
    return [[a, b], [c, d]]


def hill_inverse(m):
    a, b = m[0]
    c, d = m[1]
    det = (a * d - b * c) % 26
    inv = inverse_mod26(det)
    return [[(d * inv) % 26, (-b * inv) % 26], [(-c * inv) % 26, (a * inv) % 26]]


def hill_appliquer(texte, m):
    resultat = ""
    for i in range(0, len(texte), 2):
        x = ALPHABET.index(texte[i])
        y = ALPHABET.index(texte[i + 1])
        resultat += ALPHABET[(m[0][0] * x + m[0][1] * y) % 26]
        resultat += ALPHABET[(m[1][0] * x + m[1][1] * y) % 26]
    return resultat


def hill_chiffrer(texte, texte_cle):
    m = hill_cle(texte_cle)
    texte = nettoyer(texte)
    if len(texte) % 2 != 0:
        texte += "X"
    return hill_appliquer(texte, m)


def hill_dechiffrer(texte, texte_cle):
    m = hill_inverse(hill_cle(texte_cle))
    texte = nettoyer(texte)
    if len(texte) % 2 != 0:
        raise ValueError("Le texte chiffre doit avoir un nombre pair de lettres")
    return hill_appliquer(texte, m)
