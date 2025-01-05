class ValidationError(Exception):  # 400
    pass


class NotFound(Exception):  # 404
    pass


class AlreadyExists(Exception):  # 409
    pass


class InternalServerError(Exception):  # 500
    pass
