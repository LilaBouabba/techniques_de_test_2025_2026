"""Core triangulation logic and binary formats."""

from __future__ import annotations

import struct

Point = tuple[float, float]
Triangle = tuple[int, int, int]


class Triangulator:
    """Encode/decode point sets and triangles, and compute triangulations."""

    # === PointSet ==========================================================

    def encode_point_set(self, points: list[Point]) -> bytes:
        """Encode a list of points into the compact PointSet binary format."""
        count = len(points)
        buffer = struct.pack("<I", count)
        for x, y in points:
            buffer += struct.pack("<ff", x, y)
        return buffer

    def decode_point_set(self, buffer: bytes) -> list[Point]:
        """Decode a PointSet binary buffer into a list of points.

        Raises:
            ValueError: If the buffer length does not match the expected size.

        """
        if len(buffer) < 4:
            msg = "Buffer too short to contain point count."
            raise ValueError(msg)

        (count,) = struct.unpack_from("<I", buffer, 0)
        expected_len = 4 + count * 8

        if len(buffer) != expected_len:
            msg = f"Invalid buffer length {len(buffer)} (expected {expected_len})."
            raise ValueError(msg)

        points: list[Point] = []
        offset = 4
        for _ in range(count):
            x, y = struct.unpack_from("<ff", buffer, offset)
            offset += 8
            points.append((x, y))

        return points

    # === Triangles =========================================================

    def encode_triangles(
        self,
        vertices: list[Point],
        triangles: list[Triangle],
    ) -> bytes:
        """Encode vertices and triangles into the Triangles binary format.

        The format is:
        - PointSet part for vertices.
        - 4 bytes: triangle count (unsigned int, LE).
        - For each triangle: 3 * 4 bytes (vertex indices as unsigned ints).
        """
        n_vertices = len(vertices)

        for a, b, c in triangles:
            if not (
                0 <= a < n_vertices
                and 0 <= b < n_vertices
                and 0 <= c < n_vertices
            ):
                msg = "Triangle vertex index out of bounds."
                raise ValueError(msg)

        buffer = self.encode_point_set(vertices)
        buffer += struct.pack("<I", len(triangles))

        for a, b, c in triangles:
            buffer += struct.pack("<III", a, b, c)

        return buffer

    def decode_triangles(self, buffer: bytes) -> tuple[list[Point], list[Triangle]]:
        """Decode the Triangles binary format into vertices and triangles.

        Returns:
            A tuple (vertices, triangles).

        Raises:
            ValueError: If the buffer is not structurally valid.

        """
        if len(buffer) < 4:
            msg = "Buffer too short to contain vertices."
            raise ValueError(msg)

        (vertex_count,) = struct.unpack_from("<I", buffer, 0)
        vertex_part_len = 4 + vertex_count * 8

        if len(buffer) < vertex_part_len + 4:
            msg = "Buffer too short to contain triangle count."
            raise ValueError(msg)

        vertices = self.decode_point_set(buffer[:vertex_part_len])

        offset = vertex_part_len
        (tri_count,) = struct.unpack_from("<I", buffer, offset)
        offset += 4

        expected_total_len = vertex_part_len + 4 + tri_count * 12
        if len(buffer) != expected_total_len:
            msg = (
                "Invalid buffer length for triangles: "
                f"{len(buffer)} (expected {expected_total_len})."
            )
            raise ValueError(msg)

        triangles: list[Triangle] = []
        for _ in range(tri_count):
            a, b, c = struct.unpack_from("<III", buffer, offset)
            offset += 12
            triangles.append((a, b, c))

        return vertices, triangles

    # === Triangulation =====================================================

    @staticmethod
    def _triangle_area(p1: Point, p2: Point, p3: Point) -> float:
        """Return the signed area of triangle (p1, p2, p3)."""
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
        return 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

    def triangulate(self, points: list[Point]) -> list[Triangle]:
        """Compute a simple triangulation of the given points.

        The algorithm is intentionally simple:

        - < 3 points: no triangles.
        - 3 points: one triangle if non-collinear, otherwise none.
        - >= 4 points: fan triangulation (0, i, i+1), skipping degenerate
          triangles where two vertices share the same coordinates.
        """
        n = len(points)
        if n < 3:
            return []

        if n == 3:
            area = self._triangle_area(points[0], points[1], points[2])
            if abs(area) < 1e-12:
                return []
            return [(0, 1, 2)]

        triangles: list[Triangle] = []
        for i in range(1, n - 1):
            a, b, c = 0, i, i + 1

            if (
                points[a] == points[b]
                or points[b] == points[c]
                or points[a] == points[c]
            ):
                continue

            triangles.append((a, b, c))

        return triangles
