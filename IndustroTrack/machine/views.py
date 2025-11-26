from django.urls import reverse
from rest_framework.response import Response
import requests
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .models import  Device, DeviceLog, DeviceType
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogSerializer
from django.core.cache import cache
# from .tasks import process_receive_send_data


# Create your views here.


class CreateDevice(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAdminUser]


class CreateDeviceLog(CreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    # permission_classes = [IsAdminUser]


class CreateDeviceType(CreateAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    # permission_classes = [IsAdminUser]


class DetailDevice(RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):

        response = self.retrieve(request, *args, **kwargs)

        data = response.data
        url_path = reverse("machine:show_data")
        target_url = request.build_absolute_uri(url_path)

        requests.post(target_url, json=data)

        cache.set('cached_data', data, timeout=20)

        return Response({"sent_to": target_url, "data": data})


class ShowDataView(APIView):
    def post(self, request, *args, **kwargs):
        # received_data = request.data  # this contains the JSON sent by DetailDevice
        # serializer = DeviceSerializer(ReceiveData)
        received_data = cache.get('cached_data')

        if received_data:
            return Response({
                "message": "Data received successfully",
                "received_data": received_data  # make sure to return the variable
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Failed Receiving data!",
                "received_data": received_data  # make sure to return the variable
            }, status=status.HTTP_404_NOT_FOUND)


# @api_view(["GET"])
# def test_send(request):
#     # process_receive_send_data.delay()
#     return Response({"message": "Task triggered"})



class SendDate(APIView):
    permission_classes = [IsAdminUser]

    
class ReceivedData(APIView):
    permission_classes = [IsAdminUser]


