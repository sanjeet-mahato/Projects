class UsernameAlreadyExists(Exception):
    pass


class EmailAlreadyExists(Exception):
    pass


class InvalidVerificationToken(Exception):
    pass


class AuthenticationRequired(Exception):
    pass