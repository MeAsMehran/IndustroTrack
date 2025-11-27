from rest_framework import serializers
from .models import Device, DeviceLog, DeviceType



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



class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = '__all__'


class DeviceTypeOutputSerializer(serializers.Serializer):

    class Meta:
        model = DeviceType
        fields = ('parameter', 'code')


class DeviceOutputSerializer(serializers.Serializer):
    device_type = DeviceTypeOutputSerializer(many=True) 

    class Meta:
        model = Device
        fields = ('code', 'name', 'device_type')


class DataSerializerSerializer(serializers.Serializer):
    machine_code = serializers.CharField()
    machine_name = serializers.CharField()
    device_type = DeviceTypeSerializer(many=True)

    class Meta:
        fields = ('machine_code', 'machine_name', 'device_type')
