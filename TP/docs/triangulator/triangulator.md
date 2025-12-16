Module triangulator.triangulator
================================
Core triangulation logic and binary formats.

Classes
-------

`Triangulator()`
:   Encode/decode point sets and triangles, and compute triangulations.

    ### Methods

    `decode_point_set(self, buffer: bytes) ‑> list[tuple[float, float]]`
    :   Decode a PointSet binary buffer into a list of points.
        
        Raises:
            ValueError: If the buffer length does not match the expected size.

    `decode_triangles(self, buffer: bytes) ‑> tuple[list[tuple[float, float]], list[tuple[int, int, int]]]`
    :   Decode the Triangles binary format into vertices and triangles.
        
        Returns:
            A tuple (vertices, triangles).
        
        Raises:
            ValueError: If the buffer is not structurally valid.

    `encode_point_set(self, points: list[Point]) ‑> bytes`
    :   Encode a list of points into the compact PointSet binary format.

    `encode_triangles(self, vertices: list[Point], triangles: list[Triangle]) ‑> bytes`
    :   Encode vertices and triangles into the Triangles binary format.
        
        The format is:
        - PointSet part for vertices.
        - 4 bytes: triangle count (unsigned int, LE).
        - For each triangle: 3 * 4 bytes (vertex indices as unsigned ints).

    `triangulate(self, points: list[Point]) ‑> list[tuple[int, int, int]]`
    :   Compute a simple triangulation of the given points.
        
        The algorithm is intentionally simple:
        
        - < 3 points: no triangles.
        - 3 points: one triangle if non-collinear, otherwise none.
        - >= 4 points: fan triangulation (0, i, i+1), skipping degenerate
          triangles where two vertices share the same coordinates.