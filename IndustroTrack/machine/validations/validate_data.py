from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from machine.models import Device, DeviceType, DeviceLog


def validate_data(data):

    """
        - getting the attributes we want to check from the data
        - check if the attributes are availabe in the db or not:
            - availabe -> Do nothing and hold that object in a variable
            - not availabe -> get 404 error!
        - renew the data with device and device_type attributes
        - return the data for creation
    """
    
    device_name = data.get('device')
    device_type_name = data.get('device_type')

    device = get_object_or_404(Device, name=device_name) 
    device_type = get_object_or_404(DeviceType, parameter=device_type_name)

    availabe_device_type_ids = list(device.device_type.all().values_list('id', flat=True))

    if device_type.id not in availabe_device_type_ids:
        raise ValidationError("The Device doesn't have this data type!")

    data['device'] = device
    data['device_type'] = device_type
    
    return data
    
