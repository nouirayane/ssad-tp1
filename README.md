# TP1 SSAD - Framework de chiffrement

Partie 1 : interface (Chiffrement/Dechiffrement, Mots de passe, Attaques, Authenticite/Integrite)

Partie 2 : chiffrement et dechiffrement d'un message envoye par A a B avec :
- Cesar (decalage de n rangs, gauche -> droite ou droite -> gauche)
- Playfair
- Hill (matrice 2x2 ou 3x3)

Traitement des failles :
- Cesar : alphabet etendu (63 symboles), espaces chiffres, cles faibles refusees
- Playfair : matrice 6x6 (lettres + chiffres, plus de confusion I/J), suppression du bourrage
- Hill : alphabet de 29 symboles (A-Z, espace, point, virgule) pour garder les espaces, verification du determinant modulo 29, matrice identite refusee, matrice 3x3 possible

## Lancement

```
python interface.py
```
