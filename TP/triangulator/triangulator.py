import pytest



class Triangulator:

    def decode_point_set(self, buffer: bytes):
        raise NotImplementedError("decode_point_set not implemented yet")

    def encode_point_set(self, points):
        raise NotImplementedError("encode_point_set not implemented yet")

    def triangulate(self, points):
        raise NotImplementedError("triangulate not implemented yet")

    def encode_triangles(self, vertices, triangles):
        raise NotImplementedError("encode_triangles not implemented yet")

    def decode_triangles(self, buffer: bytes):
        raise NotImplementedError("decode_triangles not implemented yet")
