# TODO   Plan de test Triangulator 


# Objectif

L’objectif est de vérifier le bon fonctionnement du microservice Triangulator, qui :

-récupère un ensemble de points (PointSet) via le PointSetManager (connecté à la base de données),

-calcule la triangulation correspondante,

_renvoie le résultat sous forme binaire (Triangles),

-et gère correctement les erreurs possibles.


# Types de tests prévus:

 ## Tests unitaires

Ces tests porteront sur les fonctions internes du Triangulator :

   ### Conversion binaire (PointSet / Triangles)

-Vérifier que l’encodage et le décodage sont corrects et cohérents.

-Cas limites : 0 point, données invalides, valeurs extrêmes, etc.

     
   ### Algorithme de triangulation

-Vérifier que la triangulation est correcte pour des jeux de points simples (3 ou 4 points).

-Cas particuliers : points doublons, alignés, vides, ou malformés.

-Vérifier que les indices des triangles sont valides et que les triangles ne se croisent pas.

Ces tests permettent de valider la logique interne sans dépendre d’autres services.

## Test d'API

Ces tests vérifieront le bon comportement de l’API HTTP décrite dans triangulator.yml.

Cas principaux :GET /triangulation/{pointSetId} :

-400 Bad Request → si l’UUID est invalide.

-404 Not Found → si le PointSet n’existe pas.

-503 Service Unavailable → si le PointSetManager (ou la base) est indisponible.

-200 OK → si la triangulation est calculée avec succès, avec une réponse binaire correcte.

On utilisera le Flask test client pour simuler les appels HTTP.

## Test d'intégration:
Le Triangulator dépend du PointSetManager (qui lui dépend d’une base de données).
Pour tester cette intégration sans dépendre d’un vrai service, on créera un faux PointSetManager (mock) qui simulera ses réponses.

Cas prévus :

-Le PointSetManager renvoie un PointSet binaire valide → la triangulation réussit.

-Le PointSetManager renvoie 404 ou 503 → le Triangulator réagit avec le bon code HTTP.

-Le PointSetManager renvoie un binaire invalide → erreur 400 ou 500 selon le cas.

Ces tests permettent de vérifier que les composants communiquent correctement entre eux.

## Test de performance
Mesurer le comportement du Triangulator sur des ensembles de points de différentes tailles (100, 1 000, 10 000).
On observera :

-Le temps de conversion binaire (encode / decode).
-Le temps de triangulation.
-Les tests de performance seront marqués séparément pour pouvoir être exclus des tests normaux.

# Cas d’erreur à couvrir

-PointSetID au mauvais format (UUID invalide).

-PointSet inexistant dans la base.

-PointSetManager ou base de données indisponible.

-Données binaires invalides (mauvais format, taille incohérente).

-Erreur interne de calcul (ex. tous points alignés).

Chaque situation doit être testée avec le code d’erreur HTTP approprié.

=> Comme objectif final on doit s'assurer que tous les cas fonctionnels et d'erreurs sont couvert, que els test d'intégration valident la communication avec la base; que la couverture du code est sup à 85%