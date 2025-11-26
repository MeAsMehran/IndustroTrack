
from celery import shared_task
from .models import Device
import requests
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse


# from celery import shared_task

@shared_task(name='machine.tasks.send_cached_device_data')
def send_cached_device_data():
    # print("Running send_cached_device_data")
    # device = Device.objects.get(pk=1)
    #
    # data = {
    #     'device_id': device.id,
    #     'device_name': device.name,
    #     'device_code': device.code,
    #     # 'device_type': device.device_type,
    # }
    #
    # url_path = "http://localhost:8000" + reverse('machine:show_data')
    #
    #
    # cache.set("cached_data", data, timeout=20)
    # print(data)
    # requests.post(url=url_path, json=data)

    print("=========== HELLO HERE =========")



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

