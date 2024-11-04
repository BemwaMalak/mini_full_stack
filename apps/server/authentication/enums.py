from enum import Enum


class Message(Enum):
    INVALID_CREDENTIALS = "Invalid credentials"
    LOGIN_SUCCESS = "Login successful"
    VALIDATION_ERROR = "Validation error"
    TOO_MANY_REQUESTS = "Too many requests. Please try again later."
    ACCOUNT_LOCKED = (
        "Your account has been locked due to too many failed login attempts."
    )
    LOGOUT_SUCCESS = "Logout successful"
    NOT_AUTHENTICATED = "User not authenticated"
    UNAUTHORIZED = "Unauthorized access."
    FORBIDDEN = "You do not have permission to perform this action."
