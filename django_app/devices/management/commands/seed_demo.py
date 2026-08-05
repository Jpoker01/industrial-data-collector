import os
 
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
 
from devices.models import Device
 
User = get_user_model()
 
DEVICES = [
    {"name": "BTC Publisher", "serial_number": "SN-001", "protocol": "mqtt", "client_id": "pub-1"},
    {"name": "ETH Publisher", "serial_number": "SN-002", "protocol": "mqtt", "client_id": "pub-2"},
    {"name": "Modbus Server", "serial_number": "SN-003", "protocol": "modbus", "client_id": "modbus-srv-1"},
]
 
class Command(BaseCommand):
    """Create a demo superuser and device records. Safe to run repeatedly."""
 
    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
 
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'"))
        else:
            self.stdout.write(f"Superuser '{username}' already exists")
 
        for device in DEVICES:
            _, created = Device.objects.get_or_create(
                client_id=device["client_id"], defaults=device
            )
            self.stdout.write(("Created " if created else "Exists: ") + device["client_id"])
 