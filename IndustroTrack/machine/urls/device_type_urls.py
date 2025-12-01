from django.urls import path

from machine.views import CreateDeviceType, ListDeviceType, DeleteDeviceType, DetailDeviceType, \
    UpdateDeviceType

app_name='machine'

urlpatterns = [

    # DeviceType api:
    path('device_type/create/', CreateDeviceType.as_view(), name='create_device_type'),
    path('device_type/list/', ListDeviceType.as_view(), name='list_device_type'),
    path('device_type/delete/<int:id>/', DeleteDeviceType.as_view(), name='delete_device_type'),
    path('device_type/retrieve/<int:id>/', DetailDeviceType.as_view(), name='detail_device_type'),
    path('device_type/update/<int:id>/', UpdateDeviceType.as_view(), name='update_device_type'),

]
