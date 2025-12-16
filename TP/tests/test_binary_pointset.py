import pytest
from triangulator.triangulator import Triangulator


def test_pointset_roundtrip():
    """On test l'encodage et le decodage d'un point set."""
    t = Triangulator()
    points = [(0.0, 0.0), (1.0, 1.0)]
    buf = t.encode_point_set(points)
    decoded = t.decode_point_set(buf)
    assert decoded == points

def test_pointset_empty():
    """On test l'encodage et le decodage d'un point set vide."""
    t = Triangulator()
    buf = t.encode_point_set([])
    decoded = t.decode_point_set(buf)
    assert decoded == []

def test_pointset_invalid_buffer():
    """Cas ou le buffer est invalide."""
    t = Triangulator()
    bad_buf = b"\x02\x00\x00\x00"  # annonce 2 points mais aucune donnée
    with pytest.raises(Exception):
        t.decode_point_set(bad_buf)


def test_pointset_extreme_values():
    """Cas avec des valeurs extremes."""
    t = Triangulator()
    points = [(-1e9, 1e9), (3.14e6, -2.7e6)]
    buf = t.encode_point_set(points)
    decoded = t.decode_point_set(buf)
    assert decoded == points