from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    instructions = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="medications/images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        UserModel,
        null=True,
        on_delete=models.SET_NULL,
        related_name="added_medications",
    )

    def __str__(self):
        return f"{self.name} - {self.dosage}"


class RefillRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]

    user = models.ForeignKey(
        UserModel, null=True, on_delete=models.SET_NULL, related_name="refill_requests"
    )
    medication = models.ForeignKey(
        Medication, on_delete=models.CASCADE, related_name="refill_requests"
    )
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RefillRequest({self.user.username}, {self.medication.name}, {self.status})"
