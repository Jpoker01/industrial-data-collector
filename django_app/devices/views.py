"""
REST API views for devices and sending commands to publisher MQTT clients
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Command, Device
from .mqtt_client import publish_command
from .serializers import DeviceSerializer

ALLOWED_COMMANDS = {"start", "stop"}


class DeviceListView(generics.ListAPIView):
    """API endpoint for retrieving a list of devices stored in PostgreSQL"""

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetailView(generics.RetrieveAPIView):
    """API endpoint for retrieving details about a single device"""

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceCommandView(APIView):
    """API endpoints for sending control commands to MQTT publishing devices"""

    def post(self, request, pk: int) -> Response:
        device = get_object_or_404(Device, pk=pk)
        command = request.data.get("command")

        if command not in ALLOWED_COMMANDS:
            return Response(
                {"error": f"Invalid command. Allowed: {sorted(ALLOWED_COMMANDS)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cmd = Command.objects.create(
            device=device,
            command=command,
            issued_by=request.user if request.user.is_authenticated else None,
        )
        publish_command(device.client_id, command)
        cmd.published = True
        cmd.save()

        return Response(
            {"status": "sent", "device": device.client_id, "command": command},
            status=status.HTTP_202_ACCEPTED,
        )
