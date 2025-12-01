from django.urls import path

from machine.views import CreateDevice, DetailDevice, ListDevice, \
    DeleteDevice, UpdateDevice

app_name='machine'

urlpatterns = [

    # Device api:
    path('device/create/', CreateDevice.as_view(), name='create_device'),
    path('device/retrieve/<int:id>/', DetailDevice.as_view(), name='detail_device'),
    path('device/list/', ListDevice.as_view(), name='list_device'),
    path('device/delete/<int:id>/', DeleteDevice.as_view(), name='delete_device'),
    path('device/update/<int:id>/', UpdateDevice.as_view(), name='update_device'),

]
