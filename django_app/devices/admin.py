from django.contrib import admin

from .models import Command, Device


class CommandAdmin(admin.ModelAdmin):
    list_display = ("command", "device", "issued_by", "issued_at", "published")
    list_filter = ("command", "published", "issued_at")


admin.site.register(Device)
admin.site.register(Command, CommandAdmin)
