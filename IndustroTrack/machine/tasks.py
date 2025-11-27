
from celery import shared_task
from .models import Device
import requests
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse
from .service import DeviceService
from django.conf import settings


# from celery import shared_task

# @shared_task(name='machine.tasks.send_cached_device_data')
# def send_cached_device_data():
#     print("Running send_cached_device_data")
#     device = Device.objects.get(pk=1)
#
#     data = {
#         'device_id': device.id,
#         'device_name': device.name,
#         'device_code': device.code,
#         # 'device_type': device.device_type,
#     }
#
#     url_path = settings.BASE_BACKEND_URL + reverse('machine:show_data')
#
#
#     cache.set("cached_data", data, timeout=20)
#     print(data)
#     requests.post(url=url_path, json=data)


# @shared_task(name='machine.tasks.fetch_data_and_send')
# def fetch_data_and_send(machine_id):
#
#     # machine = Device.objects.get(pk=2)
#     print(90*"#")
#     fetch_path = settings.BASE_BACKEND_URL + reverse('machine:detail_device', kwargs={'id': machine_id})
#     response = requests.get(url=fetch_path, timeout=5)       # send a request to api to fetch the device info
#     response.raise_for_status()
#
#     data = response.json()
#
#     send_path = settings.BASE_BACKEND_URL + reverse('machine:create_device_log')
#     post_req = requests.post(url=send_path, json=data, timeout=5)
#     post_req.raise_for_status()
#
#     post_req.json()


# @shared_task(name='machine.tasks.fetch_machine_status')
# def fetch_machine_status():
#     print("Running fetch_machine_status")
#
#     machine = Device.objects.get(pk=1)
#
#
#     result = DeviceService.process_machine(machine_id=1)
#
#     machine_id = result['machine_id']
#     status = result['status']
#     data  = result['data']
#
#
#     if status == 'Offline':
#         print("Machine is offline")
#
#     if status == 'Online':
#         print("Machine is online")




# response = self.retrieve(request, *args, **kwargs)
#
#         data = response.data
#         url_path = reverse("machine:show_data")
#         target_url = request.build_absolute_uri(url_path)
#
#         requests.post(target_url, json=data)
#
#         cache.set('cached_data', data, timeout=20)
#
#         return Response({"sent_to": target_url, "data": data})

