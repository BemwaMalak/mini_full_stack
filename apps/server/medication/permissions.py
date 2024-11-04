from rest_framework.permissions import BasePermission


class HasMedicationPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "POST":
            return user.has_perm("medication.add_medication")
        elif method == "DELETE":
            return user.has_perm("medication.delete_medication")
        elif method == "PUT":
            return user.has_perm("medication.change_medication")
        elif method == "GET":
            return user.has_perm("medication.view_medication")
        return False


class HasRefillRequestPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "POST":
            return user.has_perm("medication.add_refillrequest")
        elif method == "PUT":
            return user.has_perm("medication.change_refillrequest")
        elif method == "GET":
            return user.has_perm("medication.view_refillrequest")
        return False
