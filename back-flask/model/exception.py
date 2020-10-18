
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

    def __init__(self, object_id: str):
        self.object_id: str = object_id

class UnexpectedRequestStatusError(RuntimeError):

    def __init__(self, actual: int, expected: int):
        self.actual: int = actual
        self.expected: int = expected
