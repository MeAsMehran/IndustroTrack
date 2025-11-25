
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from .models import  Device, DeviceLog, DeviceType
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogSerializer


# Create your views here.


class CreateDevice(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAdminUser]


class CreateDeviceLog(CreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    permission_classes = [IsAdminUser]


class CreateDeviceType(CreateAPIView):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAdminUser]









