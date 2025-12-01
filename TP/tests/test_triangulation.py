from triangulator.triangulator import Triangulator

def test_triangulate_three_points():
    """ quand on a 3 points non colineaires, on obtient un triangle."""

    t = Triangulator()
    points = [(0,0), (1,0), (0,1)]
    triangles = t.triangulate(points)
    assert triangles == [(0,1,2)]

def test_triangulate_colinear():
    """3 colinear points → no triangles."""
    t = Triangulator()
    points = [(0,0), (1,1), (2,2)]
    assert t.triangulate(points) == []

def test_triangulate_square():
    """ quand on a 4 points formant un carre, on obtient 2 triangles."""
    t = Triangulator()
    points = [(0,0), (1,0), (1,1), (0,1)]
    triangles = t.triangulate(points)
    assert len(triangles) == 2


def test_triangulate_zero_points():
    """0 point → no triangles."""
    t = Triangulator()
    assert t.triangulate([]) == []

def test_triangulate_one_point():
    """1 point → no triangles."""
    t = Triangulator()
    assert t.triangulate([(0, 0)]) == []

def test_triangulate_two_points():
    """2 points → no triangles."""
    t = Triangulator()
    assert t.triangulate([(0, 0), (1, 1)]) == []

def test_triangulate_duplicate_points():
    """Duplicate points → no invalid triangles."""
    t = Triangulator()
    points = [(0,0), (1,0), (1,1), (0,1), (0,0)]  # duplicate point
    triangles = t.triangulate(points)
    # On ne connaît pas la triangulation exacte, mais on sait :
    # 1. pas d'indice hors limite
    # 2. pas de triangle degenerate
    for a, b, c in triangles:
        assert a != b != c
        assert a < len(points) and b < len(points) and c < len(points)
