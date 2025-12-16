Module triangulator.clients
===========================
Client interface for communicating with the PointSetManager service.

Classes
-------

`PointSetManagerClient(base_url: str)`
:   Client used to retrieve PointSet binary data from the PointSetManager.
    
    Initialize the client with the PointSetManager base URL.

    ### Methods

    `get_point_set(self, point_set_id: str) ‑> bytes`
    :   Return the PointSet binary buffer for the given identifier.
        
        In the context of this TP, this method is intentionally not implemented
        and is mocked in the tests to simulate different scenarios.
        
        Raises:
            NotImplementedError: Always raised in this implementation.