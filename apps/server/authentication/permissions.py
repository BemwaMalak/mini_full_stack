from rest_framework.permissions import BasePermission


class HasRegisterPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        method = request.method

        if method == "POST":
            return user.has_perm("authentication.add_user")
        return False
