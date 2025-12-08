from rest_framework import serializers
from .models import Device, DeviceLog, DeviceType
from django.utils import timezone
from .validations.validate_data import validate_data



class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'
        

class DeviceSerializer(serializers.ModelSerializer):
    device_type = serializers.StringRelatedField(many=True, read_only=True)

    device_type_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DeviceType.objects.all(),
        write_only=True
    )
    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        device_type_ids = validated_data.pop('device_type_ids', [])
        device = Device.objects.create(**validated_data)
        device.device_type.set(device_type_ids)
        return device


class DeviceLogCreateSerializer(serializers.Serializer):
    
    device_id = serializers.CharField()
    device_type_id = serializers.CharField()
    value = serializers.FloatField()
    time = serializers.DateTimeField(default=0)
    class Meta:
        modle = DeviceLog
        fields = ('device_id', 'device_type_id', 'value', 'time')


class DeviceLogListSerializer(serializers.ModelSerializer):

    device_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False,
        required=True,
    )
    device_type_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
        required=False
    )

    pagination = serializers.IntegerField(required=False, allow_null=True)
    order_by = serializers.CharField(required=False, allow_null=True)
    search = serializers.CharField(required=False, allow_null=True)

    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = DeviceLog
        fields = ('device_ids', 'device_type_ids', 'pagination', 'order_by','search','start_date', 'end_date')


class ReceiveDataSerializer(serializers.Serializer):
    device = serializers.CharField(required=True)
    device_type = serializers.CharField(required=True)
    value = serializers.FloatField(default=0)
    time = serializers.DateTimeField()

    def validate(self, attrs):
        return validate_data(attrs)

    def create(self, validated_data):
        return DeviceLog.objects.create(**validated_data)


class DeviceNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name')


class DeviceTypeNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'parameter')


class DeviceLogOutputSerializer(serializers.Serializer):

    device = DeviceNestedSerializer()
    device_type = DeviceTypeNestedSerializer()
    time = serializers.DateTimeField()
    value = serializers.FloatField()

    class Meta:
        fields = ('id', 'device', 'device_type', 'time', 'value')


# For PUT request method
class DeviceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceTypeUpdateSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = DeviceType
            fields = ('parameter', 'code', 'des')

        def validate(self, data):
            return validate_data(data)






