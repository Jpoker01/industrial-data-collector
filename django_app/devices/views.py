from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Device, Command
from .serializers import DeviceSerializer
from .mqtt_client import publish_command

ALLOWED_COMMANDS = {"start", "stop"}


class DeviceListView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetailView(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceCommandView(APIView):
    def post(self, request, pk):
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