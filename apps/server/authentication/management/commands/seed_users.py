import random
import string
from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = "Seed the database with random users"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=10, help="Number of users to create"
        )

    def handle(self, *args, **options):
        count = options['count']
        created_users = []

        for _ in range(count):
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            email = f"{username.lower()}@example.com"
            role = random.choice([User.Role.USER, User.Role.ADMIN])
            password = "password123"

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )
            created_users.append(user.username)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} users: {", ".join(created_users)}')
        )
