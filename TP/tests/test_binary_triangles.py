import pytest
from triangulator.triangulator import Triangulator


def test_triangles_roundtrip():
    """Quand on encode et decode des triangles, on retrouve les memes."""
    t = Triangulator()
    vertices = [(0,0), (1,0), (0,1)]
    triangles = [(0,1,2)]
    buf = t.encode_triangles(vertices, triangles)
    v2, t2 = t.decode_triangles(buf)
    assert v2 == vertices
    assert t2 == triangles

def test_triangles_invalid_buffer():
    """Cas ou le buffer est invalide."""
    t = Triangulator()
    bad_buf = b"\x01\x00\x00\x00"  # trop court
    with pytest.raises(Exception):
        t.decode_triangles(bad_buf)

def test_triangles_index_error():
    """Cas ou les indices de triangles sont hors borne."""
    t = Triangulator()
    vertices = [(0,0), (1,0), (0,1)]
    triangles = [(0,1,5)]  # 5 hors borne
    with pytest.raises(Exception):
        t.encode_triangles(vertices, triangles)


def test_multiple_triangles_roundtrip():
    """Cas ou on a plusieurs triangles."""
    t = Triangulator()
    vertices = [(0,0), (1,0), (1,1), (0,1)]
    triangles = [(0,1,2), (0,2,3)]
    buf = t.encode_triangles(vertices, triangles)
    v2, t2 = t.decode_triangles(buf)
    assert v2 == vertices
    assert t2 == triangles