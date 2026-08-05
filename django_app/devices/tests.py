from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Device


class DeviceAPITests(TestCase):
    def setUp(self):
        """Set up test data and authenticate the API client."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testadmin', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.device = Device.objects.create(
            name="Test MQTT Device",
            serial_number="SN-12345",
            protocol="mqtt",
            client_id="test-client-1"
        )

    def test_get_device_list(self):
        """Test retrieving the list of devices."""
        response = self.client.get(reverse('device-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_id'], 'test-client-1')

    @patch('devices.views.publish_command')
    def test_post_valid_command(self, mock_publish):
        """Test sending a valid command to a device."""
        url = reverse('device-command', kwargs={'pk': self.device.pk})
        response = self.client.post(url, {'command': 'stop'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        mock_publish.assert_called_once_with("test-client-1", "stop")
        
    @patch('devices.views.publish_command')
    def test_post_invalid_command(self, mock_publish):
        """Test sending an invalid command yields a 400 Bad Request."""
        url = reverse('device-command', kwargs={'pk': self.device.pk})
        response = self.client.post(url, {'command': 'explode'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_publish.assert_not_called()