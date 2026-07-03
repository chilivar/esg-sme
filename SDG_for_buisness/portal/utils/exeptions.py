from builtins import Exception

class UserExistsException(Exception):
    pass

class EmailSendingException(Exception):
    pass

class InvalidTokenException(Exception):
    pass