class WindsorAIError(Exception):
    """Base exception for all Windsor AI errors."""

    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


"""
All following exceptions use 400 on the API side. (?)
"""


class AuthenticationError(WindsorAIError):
    """Raised when API key is missing or invalid (401)."""

    pass


# TODO:
class PermissionDeniedError(WindsorAIError):
    """Raised when access is denied (403)."""

    pass


class ConnectorNotFoundError(WindsorAIError):
    """Raised when connector does not exist in account. (404 {placeholder})"""

    pass


# TODO:
class RateLimitExceeded(WindsorAIError):
    """Raised when API rate limit is exceeded (429)."""

    pass


class ServerError(WindsorAIError):
    """Raised when Windsor.ai servers encounter an error (500+)."""

    pass
