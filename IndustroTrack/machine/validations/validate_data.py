from django.shortcuts import get_object_or_404
from machine.models import Device, DeviceType, DeviceLog


def validate_data(data):
    
    device_name = data.get('device')
    device_type_name = data.get('device_type')
    
    device = get_object_or_404(Device, name=device_name) 
    device_type = get_object_or_404(DeviceType, parameter=device_type_name)

    device_id = device.id 
    device_type_id = device_type.id


    data['device'] = device_id
    data['device_type'] = device_type_id
    
    return data
    
