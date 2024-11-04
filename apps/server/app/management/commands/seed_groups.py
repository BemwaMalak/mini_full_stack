from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from authentication.enums import UserPermissions
from authentication.models import User
from medication.enums import MedicationPermissions
from medication.models import Medication


class Command(BaseCommand):
    help = "Seeds all permission groups along with their permissions"

    def handle(self, *args, **kwargs):
        groups_permissions = {
            "Admins": [
                UserPermissions.ADD.value,
                MedicationPermissions.ADD.value,
                MedicationPermissions.VIEW.value,
            ],
            "Users": [
                MedicationPermissions.VIEW.value,
            ],
        }

        model_content_types = {
            "user": ContentType.objects.get_for_model(User),
            "medication": ContentType.objects.get_for_model(Medication),
        }

        for group_name, permissions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group {group_name}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Group {group_name} already exists")
                )

            for perm_codename in permissions:
                perm_name = perm_codename.replace("_", " ").capitalize()
                model_key = perm_codename.split("_")[-1]
                content_type = model_content_types.get(model_key)

                if content_type:
                    permissions = Permission.objects.filter(
                        codename=perm_codename, content_type=content_type
                    )
                    if permissions.exists():
                        permission = permissions.first()
                        group.permissions.add(permission)
                        self.stdout.write(
                            self.style.SUCCESS(f"Added {perm_codename} to {group_name}")
                        )
                    else:
                        permission, created = Permission.objects.get_or_create(
                            codename=perm_codename,
                            defaults={
                                "name": perm_name,
                                "content_type": content_type,
                            },
                        )
                        group.permissions.add(permission)
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created and added {perm_codename} to {group_name}"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Added {perm_codename} to {group_name}"
                                )
                            )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"Content type for {model_key} not found")
                    )

        self.stdout.write(
            self.style.SUCCESS("All groups and permissions have been seeded.")
        )
