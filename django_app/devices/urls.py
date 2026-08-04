from django.urls import path
from .views import DeviceListView, DeviceDetailView, DeviceCommandView

urlpatterns = [
    path("devices/", DeviceListView.as_view(), name="device-list"),
    path("devices/<int:pk>/", DeviceDetailView.as_view(), name="device-detail"),
    path("devices/<int:pk>/command/", DeviceCommandView.as_view(), name="device-command"),
]