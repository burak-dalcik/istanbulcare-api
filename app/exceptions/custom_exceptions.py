from fastapi import HTTPException, status


class BaseCustomException(Exception):
    """Base class for custom exceptions"""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(BaseCustomException):
    """Raised when a resource is not found"""
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with {identifier} not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class AlreadyExistsError(BaseCustomException):
    """Raised when trying to create a resource that already exists"""
    def __init__(self, resource: str, field: str, value: str):
        message = f"{resource} with {field} '{value}' already exists"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ValidationError(BaseCustomException):
    """Raised when validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class AuthenticationError(BaseCustomException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(BaseCustomException):
    """Raised when authorization fails"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class BusinessLogicError(BaseCustomException):
    """Raised when business logic validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


# Specific domain exceptions
class BlogPostNotFoundError(NotFoundError):
    def __init__(self, slug: str):
        super().__init__("Blog post", f"slug '{slug}'")


class BlogPostSlugExistsError(AlreadyExistsError):
    def __init__(self, slug: str):
        super().__init__("Blog post", "slug", slug)


class ServiceNotFoundError(NotFoundError):
    def __init__(self, slug: str):
        super().__init__("Service", f"slug '{slug}'")


class ServiceSlugExistsError(AlreadyExistsError):
    def __init__(self, slug: str):
        super().__init__("Service", "slug", slug)


class UserNotFoundError(NotFoundError):
    def __init__(self, email: str):
        super().__init__("User", f"email '{email}'")


class UserEmailExistsError(AlreadyExistsError):
    def __init__(self, email: str):
        super().__init__("User", "email", email)


class InvalidCredentialsError(AuthenticationError):
    def __init__(self):
        super().__init__("Invalid email or password")
