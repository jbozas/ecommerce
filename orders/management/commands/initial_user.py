from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    It creates the initial super user.
    """

    def handle(self, *args, **options):
        User.objects.create_user(
            'admin', 'admin@email.com', 'admin')
