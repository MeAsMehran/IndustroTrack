from django.urls import reverse
from rest_framework.response import Response
import requests
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .models import  Device, DeviceLog, DeviceType
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogSerializer
from django.core.cache import cache
from django.views import View
from django.http import JsonResponse
from .service import DeviceService
from .models import Device


# from .tasks import process_receive_send_data


# Create your views here.


class CreateDevice(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [IsAdminUser]


class ListDevice(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DetailDevice(RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'

    # def get(self, request, *args, **kwargs):
    #
    #     response = self.retrieve(request, *args, **kwargs)

        # data = response.data
        # url_path = reverse("machine:show_data")
        # target_url = request.build_absolute_uri(url_path)

        # requests.post(target_url, json=data)
        #
        # cache.set('cached_data', data, timeout=20)
        #
        # return Response({"sent_to": target_url, "data": data})



class DeleteDevice(DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'id'


class CreateDeviceType(CreateAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DetailDeviceType(RetrieveAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    lookup_field = 'id'


class ListDeviceType(ListAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeleteDeviceType(DestroyAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    lookup_field = 'id'


class CreateDeviceLog(CreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    # permission_classes = [IsAdminUser]


    # def post(self, request, *args, **kwargs):
    #     device = request.data.get('id')
    #     device_type = request.data.get('device_type', [])
    #     value = request.data.get('value', 0)
    #
    #     device = Device.objects.filter(id=device)
    #     if not device.exists:
    #         return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     logs_created = []
    #
    #     for type_id in device_type:
    #         try:
    #             device_type = DeviceType.objects.get(id=type_id)
    #         except DeviceType.DoesNotExist:
    #             continue  # skip invalid IDs
    #
    #         log = DeviceLog.objects.create(
    #             device = device,
    #             device_type = device_type,
    #             value = value,
    #         )
    #
    #         logs_created.append({
    #             "device": device.name,
    #             "device_type": device_type.parameter,
    #             "value": log.value,
    #             "time": log.time
    #         })
    #
    #     return Response({"logs_created" : logs_created}, status=status.HTTP_201_CREATED)


class DetailDeviceLog(RetrieveAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    lookup_field = 'id'


class ListDeviceLog(ListAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer


class DeleteDeviceLog(DestroyAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    lookup_field = 'id'



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


class MachineStatusView(APIView):

    def get(self, request, id):
        # machine = Device.objects.get(id=machine_id)
        result = DeviceService.process_machine(machine_id=id)

        if result is not None:
            data = result['data']
        else:
            data = {'status' : "Offline", 'message': "No data received"}

        url_path = reverse("machine:show_data")
        target_url = request.build_absolute_uri(url_path)
        requests.post(target_url, json=data)

        if data:
            return JsonResponse({
                "machine": Device.objects.get(pk=id).name,
                "status": "online",
                "data": data,
            })

        return JsonResponse({
            "machine": Device.objects.get(pk=id).name,
            "status": "offline",
            "data": None,
        })


class SendDate(APIView):
    permission_classes = [IsAdminUser]

    
class ReceivedData(APIView):
    permission_classes = [IsAdminUser]


