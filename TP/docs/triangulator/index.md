Module triangulator
===================
Triangulator micro-service public interface.

Sub-modules
-----------
* triangulator.app
* triangulator.clients
* triangulator.triangulator

Functions
---------

`create_app(psm_base_url: str | None = None) ‑> flask.app.Flask`
:   Crée l'application Flask du service Triangulator.
    
    Args:
        psm_base_url: Base URL du PointSetManager (optionnelle). Si non fournie,
            on utilise la variable d’environnement POINT_SET_MANAGER_BASE_URL,
            sinon une valeur par défaut.