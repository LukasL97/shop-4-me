
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
