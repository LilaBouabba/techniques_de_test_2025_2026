"""Flask application exposing the Triangulator HTTP API."""

from __future__ import annotations

import os
import uuid

from flask import Flask, Response, jsonify

from .clients import PointSetManagerClient
from .triangulator import Triangulator


def create_app(psm_base_url: str | None = None) -> Flask:
    """Crée l'application Flask du service Triangulator.

    Args:
        psm_base_url: Base URL du PointSetManager (optionnelle). Si non fournie,
            on utilise la variable d’environnement POINT_SET_MANAGER_BASE_URL,
            sinon une valeur par défaut.

    """
    app = Flask(__name__)

    if psm_base_url is None:
        psm_base_url = os.getenv(
            "POINT_SET_MANAGER_BASE_URL",
            "http://localhost:5001",
        )

    triangulator = Triangulator()
    psm_client = PointSetManagerClient(psm_base_url)

    @app.get("/triangulation/<pointSetId>")
    def triangulation(pointSetId: str):
        """Compute the triangulation for the PointSet identified by pointSetId."""
        # 1. Validation de l'UUID envoyé par le client
        try:
            uuid.UUID(pointSetId)
        except ValueError:
            return (
                jsonify(
                    {
                        "code": "BAD_REQUEST",
                        "message": "pointSetId doit être un UUID valide",
                    },
                ),
                400,
            )

        # 2. Récupération du PointSet auprès du PointSetManager
        try:
            pointset_bytes = psm_client.get_point_set(pointSetId)
        except FileNotFoundError:
            return (
                jsonify(
                    {"code": "NOT_FOUND", "message": "PointSet introuvable"},
                ),
                404,
            )
        except ConnectionError:
            return (
                jsonify(
                    {
                        "code": "SERVICE_UNAVAILABLE",
                        "message": "PointSetManager indisponible",
                    },
                ),
                503,
            )

        # 3. Décodage du PointSet du binaire vers Python
        try:
            points = triangulator.decode_point_set(pointset_bytes)
        except ValueError:
            return (
                jsonify(
                    {
                        "code": "BAD_POINTSET_FORMAT",
                        "message": "Format binaire de PointSet invalide",
                    },
                ),
                400,
            )

        # 4. Triangulation
        try:
            triangles = triangulator.triangulate(points)
        except Exception:
            return (
                jsonify(
                    {
                        "code": "TRIANGULATION_FAILED",
                        "message": "Erreur lors de la triangulation",
                    },
                ),
                500,
            )

        # 5. Encodage des triangles (Python -> binaire)
        triangles_bytes = triangulator.encode_triangles(points, triangles)

        # 6. Réponse binaire
        return Response(
            triangles_bytes,
            mimetype="application/octet-stream",
            status=200,
        )

    return app
