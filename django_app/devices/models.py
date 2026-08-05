"""
Database models for managing device metadata and issued control commands.
"""

from django.conf import settings
from django.db import models


class Device(models.Model):
    """Stores information about device gathering the data"""

    PROTOCOL_CHOICES = (
        ("mqtt", "MQTT"),
        ("modbus", "Modbus TCP"),
    )

    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=64, unique=True)
    protocol = models.CharField(max_length=16, choices=PROTOCOL_CHOICES)
    client_id = models.CharField(max_length=64, unique=True)
    location = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.client_id})"


class Command(models.Model):
    """tracks commands sent to MQTT publisher services"""

    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="commands"
    )
    command = models.CharField(max_length=32)
    payload = models.JSONField(default=dict, blank=True)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.command} -> {self.device.client_id}"
