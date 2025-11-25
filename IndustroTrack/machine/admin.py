from django.contrib import admin
from .models import Device, DeviceType, DeviceLog


# class DeviceTypeInline(admin.TabularInline):
#     model = DeviceType
#     extra = 1

@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('parameter', 'code', 'des')


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device_id' ,'device_type', 'time', 'value')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'des', 'device_type')
    # inlines = [DeviceTypeInline, DeviceLogInline]
    # inlines = [DeviceTypeInline, ]


