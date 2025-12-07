from django.urls import path

from machine.views import CreateDeviceLog, \
    DetailDeviceLog, ListDeviceLog, ReceiveData 

app_name='machine'

urlpatterns = [

    # DeviceLog api:
    path('device_log/create/', CreateDeviceLog.as_view(), name='create_device_log'),
    path('device_log/retrieve/<int:id>/', DetailDeviceLog.as_view(), name='detail_device_log'),
    path('device_log/list/',ListDeviceLog.as_view(), name='list_device_log'),

    path('device_log/recieve_data/', ReceiveData.as_view(), name='recieve_data'),
]
