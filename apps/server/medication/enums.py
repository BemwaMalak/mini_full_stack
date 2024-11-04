from enum import Enum


class MedicationPermissions(Enum):
    ADD = "add_medication"
    VIEW = "view_medication"
    DELETE = "delete_medication"
    CHANGE = "change_medication"


class RefillRequestPermissions(Enum):
    ADD = "add_refillrequest"
    VIEW = "view_refillrequest"
    CHANGE = "change_refillrequest"
