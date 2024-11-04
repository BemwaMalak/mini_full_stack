import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from medication.models import Medication

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample Medication records."

    def handle(self, *args, **kwargs):
        # Define sample medication data
        medications_data = [
            {
                "name": "Paracetamol",
                "dosage": "500mg",
                "quantity": 20,
                "instructions": "Take one tablet every 6 hours as needed for pain.",
            },
            {
                "name": "Ibuprofen",
                "dosage": "200mg",
                "quantity": 15,
                "instructions": "Take one tablet every 4-6 hours with food to reduce inflammation.",
            },
            {
                "name": "Amoxicillin",
                "dosage": "250mg",
                "quantity": 30,
                "instructions": "Take one capsule every 8 hours for 10 days.",
            },
            {
                "name": "Aspirin",
                "dosage": "81mg",
                "quantity": 25,
                "instructions": "Take one tablet daily for heart health, or as directed by a doctor.",
            },
            {
                "name": "Metformin",
                "dosage": "500mg",
                "quantity": 60,
                "instructions": "Take one tablet twice daily with meals to manage blood sugar levels.",
            },
        ]

        users = UserModel.objects.filter(role="ADMIN")
        if not users.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No admins found in the database. Please create at least one admin first."
                )
            )
            return

        for med_data in medications_data:
            medication, created = Medication.objects.get_or_create(
                name=med_data["name"],
                defaults={
                    "dosage": med_data["dosage"],
                    "quantity": med_data["quantity"],
                    "instructions": med_data["instructions"],
                    "added_by": random.choice(users),
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added medication: {medication.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Medication {medication.name} already exists.")
                )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))
