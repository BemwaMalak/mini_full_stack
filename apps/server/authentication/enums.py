from enum import Enum


class Message(Enum):
    INVALID_CREDENTIALS = "Invalid credentials"
    LOGIN_SUCCESS = "Login successful"
    VALIDATION_ERROR = "Validation error"
