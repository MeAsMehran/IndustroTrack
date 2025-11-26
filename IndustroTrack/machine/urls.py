from django.urls import path

from .views import CreateDevice, SendDate, ReceivedData, ShowDataView, DetailDevice

app_name='machine'

urlpatterns = [

    path('device/create/', CreateDevice.as_view(), name='create_device'),
    path('device/retrieve/<int:id>/', DetailDevice.as_view(), name='detail_device'),
    # path('test_send/', test_send, name='test_send'),
    path('show_data/', ShowDataView.as_view(), name='show_data'),

    path('send_data/', SendDate.as_view(), name='send_data'),
    path('recieve_data/', ReceivedData.as_view(), name='receive_data'),


]
