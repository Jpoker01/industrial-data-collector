from django.contrib import admin

from .models import Command, Device


class CommandAdmin(admin.ModelAdmin):
    list_display = ("command", "device", "issued_by", "issued_at")
    list_filter = ("command", "issued_at")


admin.site.register(Device)
admin.site.register(Command, CommandAdmin)
