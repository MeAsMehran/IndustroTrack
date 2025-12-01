from django.urls import path

from machine.views import SendDate, ReceivedData, ShowDataView, MachineStatusView  

app_name='machine'

urlpatterns = [

    # path('test_send/', test_send, name='test_send'),
    path('show_data/', ShowDataView.as_view(), name='show_data'),

    path('machine/status/<int:id>/', MachineStatusView.as_view(), name='machine_status'),

    path('send_data/', SendDate.as_view(), name='send_data'),
    path('recieve_data/', ReceivedData.as_view(), name='receive_data'),
]
