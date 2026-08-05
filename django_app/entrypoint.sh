#!/usr/bin/env bash
set -e

echo "Running database migrations..."
python manage.py migrate

echo "Seeding initial IoT devices..."
python manage.py shell <<EOF
from devices.models import Device

initial_devices = [
    {
        "name": "Crypto Publisher 1",
        "serial_number": "SN-CRYPTO-001",
        "protocol": "mqtt",
        "client_id": "pub-1",
        "location": "Server Room A",
    },
    {
        "name": "Crypto Publisher 2",
        "serial_number": "SN-CRYPTO-002",
        "protocol": "mqtt",
        "client_id": "pub-2",
        "location": "Server Room B",
    },
    {
        "name": "Modbus Industrial Sensor",
        "serial_number": "SN-MODBUS-999",
        "protocol": "modbus",
        "client_id": "idc-modbus-client",
        "location": "Factory Floor 1",
    },
]

for dev_data in initial_devices:
    device, created = Device.objects.get_or_create(
        client_id=dev_data["client_id"],
        defaults=dev_data,
    )
    if created:
        print(f"Created device: {device.name}")
    else:
        print(f"Device already exists: {device.name}")
EOF

echo "Attempting to create default superuser..."
python manage.py createsuperuser --noinput || true

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000