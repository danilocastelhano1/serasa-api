import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed the database information"

    def create_super_user(self):
        if User.objects.count() == 0:
            logger.info(self.style.WARNING("Creating super user..."))
            User.objects.create_superuser("admin", "admin@example.com", "123456")
            logger.info(self.style.SUCCESS("Created super user!"))

    def handle(self, *args, **options):
        self.create_super_user()
