from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError("The Username must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        USER = "USER", "User"
        ADMIN = "ADMIN", "Admin"

    username = models.CharField(unique=True, max_length=50)
    role = models.CharField(max_length=5, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Define a mapping from roles to groups
        role_group_map = {
            self.Role.USER: "Users",
            self.Role.ADMIN: "Admins",
        }

        # Get or create the group based on the user's role
        group_name = role_group_map.get(self.role)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            self.groups.add(group)
