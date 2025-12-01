import json
import uuid
import pytest
from triangulator.app import create_app
from triangulator.triangulator import Triangulator
from triangulator.clients import PointSetManagerClient



def test_invalid_uuid_returns_400():
    """quand l'UUID est invalide, on a une 400 BAD REQUEST."""
    app = create_app()
    client = app.test_client()

    resp = client.get("/triangulation/not-a-uuid")
    
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert "code" in data
    assert data["code"] == "BAD_REQUEST"



def test_psm_returns_404(monkeypatch):
    """quand le PSM ne trouve pas le PointSet, on a une 404 NOT FOUND."""
    app = create_app()
    client = app.test_client()

    # mock du PSM
    def fake_get(*args, **kwargs):
        raise FileNotFoundError("PointSet not found")

    monkeypatch.setattr(PointSetManagerClient, "get_point_set", fake_get)

    valid_uuid = str(uuid.uuid4())
    resp = client.get(f"/triangulation/{valid_uuid}")

    assert resp.status_code == 404
    data = json.loads(resp.data)
    assert data["code"] == "NOT_FOUND"



def test_psm_unavailable(monkeypatch):
    """quand le PSM est indisponible, on a une 503 SERVICE UNAVAILABLE."""
    app = create_app()
    client = app.test_client()

    def fake_get(*args, **kwargs):
        raise ConnectionError("Service unavailable")

    monkeypatch.setattr(PointSetManagerClient, "get_point_set", fake_get)

    valid_uuid = str(uuid.uuid4())
    resp = client.get(f"/triangulation/{valid_uuid}")

    assert resp.status_code == 503
    data = json.loads(resp.data)
    assert data["code"] == "SERVICE_UNAVAILABLE"


def test_invalid_binary_from_psm(monkeypatch):
    """quand le PSM renvoie un PointSet invalide, on a une 400 BAD REQUEST."""
    app = create_app()
    client = app.test_client()

    # PSM renvoie du binaire tronqué
    monkeypatch.setattr(PointSetManagerClient, "get_point_set", lambda *_: b"\x01\x00\x00")

    # mock decode_point_set pour qu’il lève une erreur
    monkeypatch.setattr(Triangulator, "decode_point_set", lambda *_, **__: (_ for _ in ()).throw(ValueError("Invalid buffer")))

    valid_uuid = str(uuid.uuid4())
    resp = client.get(f"/triangulation/{valid_uuid}")

    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert data["code"] == "BAD_POINTSET_FORMAT"



def test_triangulation_failure(monkeypatch):
    """quand la triangulation echoue, on a une 500 INTERNAL SERVER ERROR."""
    app = create_app()
    client = app.test_client()


    # PSM renvoie un PointSet correct
    monkeypatch.setattr(PointSetManagerClient, "get_point_set", lambda *_: b"\x00\x00\x00\x00")

    # decode OK, triangulate KO
    monkeypatch.setattr(Triangulator, "decode_point_set", lambda *_: [])
    monkeypatch.setattr(Triangulator, "triangulate", lambda *_: (_ for _ in ()).throw(RuntimeError("Triangulation failed")))

    valid_uuid = str(uuid.uuid4())
    resp = client.get(f"/triangulation/{valid_uuid}")

    assert resp.status_code == 500
    data = json.loads(resp.data)
    assert data["code"] == "TRIANGULATION_FAILED"


def test_successful_triangulation(monkeypatch):
    """quand tout va bien, on a une 200 OK avec les triangles binaires."""
    app = create_app()
    client = app.test_client()

    # PSM renvoie un PointSet valide
    pointset_bytes = b"\x01\x00\x00\x00" + b"\x00\x00\x80\x3f" + b"\x00\x00\x80\x3f"
    monkeypatch.setattr(PointSetManagerClient, "get_point_set", lambda *_: pointset_bytes)

    # decode OK
    monkeypatch.setattr(Triangulator, "decode_point_set", lambda *_: [(1.0, 1.0)])

    # triangulation OK
    monkeypatch.setattr(Triangulator, "triangulate", lambda *_: [(0, 0, 0)])

    # encode triangles OK (renvoie juste un buffer bidon)
    monkeypatch.setattr(Triangulator, "encode_triangles", lambda *_: b"\x01\x02\x03\x04")

    valid_uuid = str(uuid.uuid4())
    resp = client.get(f"/triangulation/{valid_uuid}")

    assert resp.status_code == 200
    assert resp.data == b"\x01\x02\x03\x04"
    assert resp.content_type == "application/octet-stream"
