"""
Serializers for converting Device model instances to and from JSON formats.
"""

from rest_framework import serializers

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer class for converting PostgreSQL Device rows to JSON representation"""

    class Meta:
        model = Device
        fields = [  # noqa: RUF012
            "id",
            "name",
            "serial_number",
            "protocol",
            "client_id",
            "location",
            "is_active",
            "created_at",
        ]
