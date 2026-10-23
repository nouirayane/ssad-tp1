# TP1 SSAD - Framework de chiffrement

Partie 1 : interface (Chiffrement/Dechiffrement, Mots de passe, Attaques, Authenticite/Integrite)

Partie 2 : chiffrement et dechiffrement d'un message envoye par A a B avec :
- Cesar (decalage de n rangs, gauche -> droite ou droite -> gauche)
- Playfair
- Hill (matrice 2x2 ou 3x3)

L'interface separe l'entite A, le canal public et l'entite B. Chaque entite a sa propre cle secrete.

Traitement des failles :
- Message mal recu par B : Playfair et Hill supprimaient les espaces, chiffres, ponctuation et minuscules.
  Les trois algorithmes utilisent maintenant un alphabet de 81 symboles (83 pour Hill), donc B recoit exactement le message de A.
- Probleme de la cle : la cle ne doit pas passer sur le canal. Echange de cle Diffie-Hellman :
  A et B envoient seulement des valeurs publiques et calculent chacun la meme cle secrete.
- Cesar : tout le message est chiffre, cles faibles refusees
- Playfair : matrice 9x9, bourrage X ou Q supprime apres le dechiffrement, cle vide refusee
- Hill : modulo 83 (premier), verification du determinant, matrice identite refusee, matrice 3x3 possible

## Lancement

```
python interface.py
```
