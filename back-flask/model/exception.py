
class UserNotFoundError(RuntimeError):
    pass

class IncorrectPasswordError(RuntimeError):
    pass

class UnexpectedUserTypeError(RuntimeError):
    pass

class UserAlreadyRegisteredError(RuntimeError):
    pass
