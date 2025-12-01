class PointSetManagerClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_point_set(self, point_set_id: str) -> bytes:
        raise NotImplementedError("PointSetManager client not implemented yet")
