from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class MeasurementAPITests(TestCase):
    def setUp(self):
        """Set up and authenticate the API client."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testadmin', password='testpassword')
        self.client.force_authenticate(user=self.user)

    @patch('measurements.views.repo.list')
    def test_get_measurements(self, mock_repo_list):
        """Test retrieving measurements from the mocked MongoDB repository."""
        mock_data = [
            {"_id": "64c8d", "source": "mqtt", "price": 50000.0, "client_id": "pub-1"}
        ]
        mock_repo_list.return_value = mock_data
        
        response = self.client.get(reverse('measurement-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['price'], 50000.0)
        self.assertEqual(response.headers.get('Refresh'), '5')