import pytest
import time
import random
from triangulator.triangulator import Triangulator


# Génération stable de points pour les tests
def generate_points(n):
    random.seed(42)  # reproductible
    return [(random.random(), random.random()) for _ in range(n)]


@pytest.mark.perf
def test_triangulation_100_points():
    """Mesure la performance de la triangulation sur 100 points."""
    t = Triangulator()
    points = generate_points(100)

    start = time.perf_counter()
    t.triangulate(points)
    duration = time.perf_counter() - start

    
    print(f"Triangulate 100 points: {duration:.6f} seconds")


@pytest.mark.perf
def test_triangulation_1000_points():
    """Mesure la performance de la triangulation sur 1 000 points."""
    t = Triangulator()
    points = generate_points(1000)

    start = time.perf_counter()
    t.triangulate(points)
    duration = time.perf_counter() - start

    print(f"Triangulate 1000 points: {duration:.6f} seconds")


@pytest.mark.perf
def test_triangulation_5000_points():
    """Mesure la performance de la triangulation sur 5 000 points."""
    t = Triangulator()
    points = generate_points(5000)

    start = time.perf_counter()
    t.triangulate(points)
    duration = time.perf_counter() - start

    print(f"Triangulate 5000 points: {duration:.6f} seconds")
