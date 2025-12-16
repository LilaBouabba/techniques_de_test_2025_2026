# TODO

# Tests mis en place

Les tests ont été organisés en trois catégories.

Les tests unitaires vérifient la logique interne du Triangulator : encodage et décodage des formats binaires (PointSet et Triangles), ainsi que le comportement de l’algorithme de triangulation sur des cas simples et des cas limites (peu de points, points alignés, carrés, doublons).

Les tests d’API, qui sont ici considérés comme des tests d’intégration, vérifient le fonctionnement global du micro-service. Ils testent l’endpoint HTTP du Triangulator et valident l’enchaînement complet des étapes : validation de l’UUID, récupération du PointSet via un client mocké, gestion des erreurs et retour d’une réponse binaire correcte.

Les tests de performance sont séparés des autres tests. Ils mesurent le temps d’exécution de la triangulation pour des ensembles de 100, 1 000 et 5 000 points, afin d’observer le comportement du service lorsque la taille des données augmente.

# Ce qui a bien fonctionné

Le plan de test rédigé au départ a aidé à structurer le travail.

La séparation entre tests unitaires, tests d’intégration et tests de performance est claire.

Le mock du PointSetManager permet de tester le Triangulator sans dépendre d’un service externe réel.

L’utilisation du Makefile simplifie l’exécution des tests et des outils de qualité.

La couverture de code est élevée (97 %), ce qui montre que les tests sont efficaces.

La documentation est générée automatiquement à partir des docstrings.

# Difficultés rencontrées

Les principales difficultés concernaient surtout les outils :

Les règles de linting étaient strictes et ont demandé de nombreuses corrections de style.

Certaines erreurs de lint étaient difficiles à comprendre au début. 

comprendre  la methode de mettre en place des tests au début 

# Ce que je ferais différemment

Avec le recul, je ferais plus attention au style du code et aux docstrings dès le début afin de limiter les corrections en fin de projet. J’intégrerais également plus tôt les contraintes liées au linting.
ausi je preterais plus attention au plan de test de base dés le début. 

# Conclusion

Ce projet m’a permis de mieux comprendre l’intérêt de tester un composant à plusieurs niveaux. Les tests unitaires assurent la fiabilité de la logique interne, les tests d’intégration valident le comportement global de l’API, et les tests de performance permettent d’observer le passage à l’échelle. Le plan de test initial était globalement adapté et a servi de guide tout au long du TP.


# Pour aller plus loin 
tout a été mieux expliqué dans le fichier rapport.pdf avec capture d'ecran de dif tests 