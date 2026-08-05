"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("devices.urls")),
    path("api/", include("measurements.urls")),
    path("api/token/", obtain_auth_token),
]
