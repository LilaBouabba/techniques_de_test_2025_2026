Module triangulator.app
=======================
Flask application exposing the Triangulator HTTP API.

Functions
---------

`create_app(psm_base_url: str | None = None) ‑> flask.app.Flask`
:   Crée l'application Flask du service Triangulator.
    
    Args:
        psm_base_url: Base URL du PointSetManager (optionnelle). Si non fournie,
            on utilise la variable d’environnement POINT_SET_MANAGER_BASE_URL,
            sinon une valeur par défaut.