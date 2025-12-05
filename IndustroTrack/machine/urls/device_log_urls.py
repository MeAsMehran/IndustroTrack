from django.urls import path

from machine.views import CreateDeviceLog, \
    DetailDeviceLog, DeleteDeviceLog, ListDeviceLog

app_name='machine'

urlpatterns = [

    # DeviceLog api:
    path('device_log/create/', CreateDeviceLog.as_view(), name='create_device_log'),
    path('device_log/retrieve/<int:id>/', DetailDeviceLog.as_view(), name='detail_device_log'),
    path('device_log/delete/<int:id>/', DeleteDeviceLog.as_view(), name='delete_device_log'),
    path('device_log/list/',ListDeviceLog.as_view(), name='list_device_log'),
]
