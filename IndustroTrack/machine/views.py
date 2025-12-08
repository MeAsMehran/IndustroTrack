from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from .models import  Device, DeviceLog, DeviceType
from rest_framework import status
from .serializers import DeviceSerializer, DeviceTypeSerializer, DeviceLogListSerializer, DeviceUpdateSerializer, \
DeviceTypeUpdateSerializer, DeviceLogOutputSerializer, DeviceLogCreateSerializer, ReceiveDataSerializer
from .models import Device
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .paginations import DeviceLogPagination
from rest_framework import serializers

# Create your views here.

class CreateDevice(CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ListDevice(ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]


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
    serializer_class = DeviceLogCreateSerializer


class DetailDeviceLog(RetrieveAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'


       

from .query.device_log_filter import dev_log_filter
class ListDeviceLog(ListAPIView):
    model = DeviceLog
    serializer_class = DeviceLogListSerializer
    pagination_class = DeviceLogPagination

    def setup(self, request, *args, **kwargs):
        self.device_logs = self.model.objects.all()
        return super().setup(request, *args, **kwargs)

    def parse_int_list(self, raw_value):
        """
        Convert comma-separated list string into list of ints.
        Example: "1,2,3" → [1, 2, 3]
        """
        if not raw_value:
            return None

        parts = raw_value.split(',')
        try:
            return [int(x.strip()) for x in parts if x.strip() != ""]
        except ValueError:
            raise serializers.ValidationError("Must be comma-separated integers, e.g. 1,2,3")
 

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='device_ids',
                in_=openapi.IN_QUERY,
                description='List of device IDs (JSON list). Example: 1,2,3',
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                name='device_type_ids',
                in_=openapi.IN_QUERY,
                description='List of device type IDs (JSON list). Example: 4,5',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='start_date',
                in_=openapi.IN_QUERY,
                description='Start date (ISO8601). Example: 2025-01-01T00:00:00',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='end_date',
                in_=openapi.IN_QUERY,
                description='End date (ISO8601). Example: 2025-06-01T00:00:00',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='order_by',
                in_=openapi.IN_QUERY,
                description='Order By',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='search from the fields: device_name, parameter_name',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                description='Return the number of the records each request or page',
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                name='page_number',
                in_=openapi.IN_QUERY,
                description='Page number for pagination',
                type=openapi.TYPE_STRING,
                required=False
            ),
        ]
    )

    
    def get(self, request):
        try:
            device_ids = self.parse_int_list(request.GET.get("device_ids"))
            device_type_ids = self.parse_int_list(request.GET.get("device_type_ids"))
        except serializers.ValidationError as exc:
            return Response({"detail": str(exc)}, status=400)

        # Build serializer params
        query_params = {
            "device_ids": device_ids,
            "device_type_ids": device_type_ids or [],
            "start_date": request.GET.get("start_date"),
            "end_date": request.GET.get("end_date"),
            "order_by": request.GET.get("order_by"),
            "search": request.GET.get("search"),
            "page_number": request.GET.get("page_number"),
            "page_size": request.GET.get("page_size"),
        }

        serializer = self.serializer_class(data=query_params)

        if not serializer.is_valid():
            return response(serializer.errors, status=status.http_400_bad_request)
     
        validated_params = serializer.validated_data

        # Filter queryset
        queryset = dev_log_filter(validated_params)

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            output = DeviceLogOutputSerializer(page, many=True)
            return paginator.get_paginated_response(output.data)

        output = DeviceLogOutputSerializer(queryset, many=True)
        return Response({"data": output.data})


class ReceiveData(CreateAPIView):
    serializer_class = ReceiveDataSerializer 
    model = DeviceLog
    queryset = DeviceLog.objects.all()


                
   

