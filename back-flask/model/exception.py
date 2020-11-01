
class UserNotFoundError(RuntimeError):
    pass

class IncorrectPasswordError(RuntimeError):
    pass

class UnexpectedUserTypeError(RuntimeError):
    pass

class UserAlreadyRegisteredError(RuntimeError):
    pass

class ShopDoesNotExistError(RuntimeError):
    pass

class UserSessionIdNotFoundError(RuntimeError):
    pass

class UnauthorizedAccessError(RuntimeError):
    pass

class ObjectIdNotFoundError(RuntimeError):

    def __init__(self, object_id: str, object_type: str):
        self.object_id: str = object_id
        self.object_type: str = object_type

class UnexpectedRequestStatusError(RuntimeError):

    def __init__(self, actual: int, expected: int):
        self.actual: int = actual
        self.expected: int = expected

class UnexpectedNumberOfLocationsForAddressError(RuntimeError):

    def __init__(self, number_of_locations: int, address: str):
        self.number_of_locations: int = number_of_locations
        self.address: str = address

class MissingDeliveryAddressError(RuntimeError):
    pass
