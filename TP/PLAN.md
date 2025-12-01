# TODO   Plan de test Triangulator 

### test unitaires 

1. Tests unitaires : Conversion binaire PointSet
## Ce que je dois tester

Encodage d’un PointSet → donne un binaire correct.

Décodage d’un PointSet → redonne la liste de points d’origine.

Round-trip :
decode(encode(points)) == points.

## Cas à tester

PointSet normal : 3–4 points simples.

PointSet vide : 0 point.

Points avec valeurs négatives ou grandes.

Données binaires tronquées → doit lever une erreur.

Nombre de points annoncé incorrect → doit lever une erreur.

2. Tests unitaires : Conversion binaire Triangles
## Ce que je dois tester

Encodage d’un ensemble (sommets, triangles).

Décodage du binaire donne les mêmes données.

Round-trip sur sommets + triangles.

## Cas à tester

1 triangle simple.

Plusieurs triangles.

Indice de triangle hors-borne → erreur.

Buffer tronqué → erreur.

3. Tests unitaires : Algorithme triangulate(points)
## Ce que je dois tester

Que l’algorithme renvoie :

le bon nombre de triangles,

uniquement des triangles valides (indices bons, aire > 0).

## Cas à tester

0 point → 0 triangle.

1 point → 0 triangle.

2 points → 0 triangle.

3 points non alignés → 1 triangle.

3 points alignés → 0 triangle.

4 points formant un carré → 2 triangles.

Points doublons → pas de triangles dégénérés.



### Tests API 

1. UUID invalide → 400 : vérifier que l’API rejette un pointSetId mal formé.

2. PSM renvoie 404 → 404 : vérifier que l’API relaie correctement “PointSet non trouvé”.

3. PSM indisponible → 503 : vérifier que l’API gère l’erreur réseau/service down.

4. Buffer invalide → 400 ou 500 : vérifier que l’API détecte un PointSet binaire corrompu.

5. Triangulation échoue → 500 : vérifier que l’API renvoie une erreur interne en cas d’échec du calcul.

6. Cas réussi → 200 + binaire : vérifier que l’API renvoie bien les triangles en format binaire.



### test performances 

Objectif : mesurer le temps d’exécution de triangulate(points) pour différentes tailles d’ensembles de points.

Tailles testées : 100 points, 1 000 points, 5 000 points.

Attendus :

la triangulation doit s’exécuter sans erreur,

le temps doit rester raisonnable (on observe les valeurs).

Approche :

générer des points (grille ou aléatoire avec graine fixe),

mesurer le temps avec perf_counter(),

exécuter triangulate(points),

marquer ces tests avec @pytest.mark.perf pour les séparer des tests unitaires.