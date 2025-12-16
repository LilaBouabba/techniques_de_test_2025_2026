"""Client interface for communicating with the PointSetManager service."""


class PointSetManagerClient:
    """Client used to retrieve PointSet binary data from the PointSetManager."""

    def __init__(self, base_url: str) -> None:
        """Initialize the client with the PointSetManager base URL."""
        self.base_url = base_url

    def get_point_set(self, point_set_id: str) -> bytes:
        """Return the PointSet binary buffer for the given identifier.

        In the context of this TP, this method is intentionally not implemented
        and is mocked in the tests to simulate different scenarios.

        Raises:
            NotImplementedError: Always raised in this implementation.

        """
        msg = "PointSetManager client not implemented yet."
        raise NotImplementedError(msg)
