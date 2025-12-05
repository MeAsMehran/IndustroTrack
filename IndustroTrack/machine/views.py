from rest_framework import serializers
from django.db.models import Avg
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
import requests
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from .models import  Device, DeviceLog, DeviceType
from rest_framework import status
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogSerializer, DeviceUpdateSerializer, \
DeviceTypeUpdateSerializer, DeviceLogOutputSerializer
from django.core.cache import cache
from django.http import JsonResponse
from .service import DeviceService
from .models import Device

# Create your views here.

class CreateDevice(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class ListDevice(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DetailDevice(RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


class DeleteDevice(DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


class UpdateDevice(APIView):
    serializer_class = DeviceUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'

    @swagger_auto_schema(request_body=DeviceUpdateSerializer)
    def put(self, request, id):
        return self.update_device(request, id, partial=False)

    @swagger_auto_schema(request_body=DeviceUpdateSerializer)
    def patch(self, request, id):
        return self.update_device(request, id, partial=True)

    def update_device(self, request, id, partial):
        device = Device.objects.filter(pk=id).first()
        if not device:
            return Response({"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceUpdateSerializer(device, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()

            if "device_type" in serializer.validated_data:
                device.device_type.set(serializer.validated_data["device_type"])

            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)


class CreateDeviceType(CreateAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DetailDeviceType(RetrieveAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


class ListDeviceType(ListAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DeleteDeviceType(DestroyAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


class UpdateDeviceType(APIView):
    serializer_class = DeviceTypeUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


    @swagger_auto_schema(request_body=DeviceTypeUpdateSerializer)
    def put(self, request, id):
        return self.update_device_type(request, id, partial=False)

    @swagger_auto_schema(request_body=DeviceTypeUpdateSerializer)
    def patch(self, request, id):
        return self.update_device_type(request, id, partial=True)

    def update_device_type(self, request, id, partial):
        device_type = DeviceType.objects.get(pk=id)
        if not device_type:
            return Response({'detail' : "Device Not Found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(device_type, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_200_OK)

        return Response(request.data, status=400)


class CreateDeviceLog(CreateAPIView):
    queryset = DeviceLog.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = DeviceLogSerializer


class DetailDeviceLog(RetrieveAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'



class ListDeviceLog(ListAPIView):
    model = DeviceLog
    serializer_class = DeviceLogSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def setup(self, request, *args, **kwargs):

        self.device_logs = self.model.objects.all()
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']    # works fine i checked it
        end_date = serializer.validated_data['end_date']        # works fine i checked it
        device_ids = serializer.validated_data.get('device_ids')
        device_type_ids = serializer.validated_data.get('device_type_ids')

        
        if device_type_ids:
            filtered_device_logs = self.device_logs.filter(
            time__range=(start_date, end_date),
            device_id__in=device_ids,
            device_type_id__in=device_type_ids,
        )
        else:
            filtered_device_logs = self.device_logs.filter(
            time__range=(start_date, end_date),
            device_id__in=device_ids,
        )
            
        output = DeviceLogOutputSerializer(filtered_device_logs, many=True)
        avg_value = filtered_device_logs.aggregate(avg_value=Avg('value'))

        return Response({'device_logs_avg_value' : avg_value["avg_value"], 'data' : output.data}, status=status.HTTP_200_OK)
        # return Response({'device_logs_avg_value' : avg_value["avg_value"], 'logs' : json_data}, status=status.HTTP_200_OK)


class DeleteDeviceLog(DestroyAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    lookup_field = 'id'



