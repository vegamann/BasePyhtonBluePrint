class ApiError(Exception):
    code = 422
    description = "Default message"

class RouteAlreadyExists(ApiError):
    code = 412
    description = "Route already exists"

class RouteNotFoundError(ApiError):
    code = 404
    description = "Route does not exist"

class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"

class InvalidParams(ApiError):
    code = 400
    description = "Bad request"

class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"

class ExternalError(ApiError):
    code = 422 # Default
    description = "External error"

    def __init__(self, code):
        self.code = code

