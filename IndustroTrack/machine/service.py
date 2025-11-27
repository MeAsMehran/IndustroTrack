from django.urls import reverse_lazy, reverse
from django.core.cache import cache
import requests
from django.conf import settings


from .models import Device


class DeviceService:



    @staticmethod
    def fetch_machine_data(machine_id):

        CACHE_TIMEOUT = 20

        try:
            url_path = settings.BASE_BACKEND_URL + reverse('machine:detail_device', kwargs={'id': machine_id})

            response = requests.get(url_path, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


    @staticmethod
    def cache_machine_data(machine_id, data):
        cache_key = f"status_machine:{machine_id}"
        cache.set(cache_key, data, timeout=DeviceService.CACHE_TIMEOUT)


    @staticmethod
    def get_machine_data(machine_id):
        cache_key = f"status_machine:{machine_id}"
        data = cache.get(cache_key)
        return data


    @staticmethod
    def process_machine(machine_id):
        # cache_key = f"status_machine:{machine_id}"
        # data = cache.get(cache_key)

        cached_data = DeviceService.get_machine_data(machine_id)


        # Offline if our cache is empty => The machine was offline
        if cached_data is None:
            # offline => We should create a stop record for the current machine with start auto_add_now and end null
            return {'status' : 'Offline',
                    'machine_id' : machine_id,
                    'data' : None
            }

        else:
            #online
            new_data = DeviceService.fetch_machine_data(machine_id)     # gives us the latest information about the machine
            if new_data is None:
                # don't know what to do
                return None
            else:
                # cache the data again


                DeviceService.cache_machine_data(machine_id, new_data)
                return {'status' : 'Online',
                        'machine_id' : machine_id,
                        'data' : new_data}
