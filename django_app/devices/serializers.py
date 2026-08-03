from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "serial_number", "protocol", "client_id",
                  "location", "is_active", "created_at"]