import time

from django.core.management import BaseCommand
from django.db import connections, InterfaceError
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for db...")

        db_ready = False
        while not db_ready:
            try:
                connections["default"].cursor()
                db_ready = True
            except (OperationalError, InterfaceError) as e:
                self.stdout.write(f"Database unavailable, waiting...{e}")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database ready!"))
