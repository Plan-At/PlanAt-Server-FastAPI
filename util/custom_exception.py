from builtins import Exception


class DemoException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TokenException(Exception):
    def __init__(self, token: str, message):
        self.token = token
        super().__init__(message)


class TokenExpiredException(TokenException):
    def __init__(self, token: str, expiration_timestamp: int, message="token expired"):
        self.expiration_timestamp = expiration_timestamp
        super().__init__(token, message)
