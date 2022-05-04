class ServiceInitializationError(Exception):
    """
    Raised when a service has an error 
    initialazing.
    """

    def __init__(self, error):
        self.error = error


class ServiceUnavailableError(Exception):
    """
    Raised when a service cannot be
    reached.
    """

    def __init__(self, error):
        self.error = error


class ProductOrStockNotFound(Exception):
    """
    Raised when a product couldn't be found
    or its stock is not enough.
    """

    def __init__(self, error):
        self.error = error


class TransactionCreationError(Exception):
    """
    """

    def __init__(self, error):
        self.error = error
