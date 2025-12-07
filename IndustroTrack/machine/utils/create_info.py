
"""
    This file creates device_log data for years 2024 and 2025
"""

# machine/utils/create_data.py

def populate_device_logs():
    import random
    from datetime import datetime, timedelta
    from machine.models import Device, DeviceType, DeviceLog

    num_entries = 10000

    # ---- DEFINE DATE RANGE ----
    start_date = datetime(2024, 1, 1, 0, 0, 0)
    end_date = datetime(2025, 12, 31, 23, 59, 59)

    total_seconds = int((end_date - start_date).total_seconds())

    devices = list(Device.objects.all())
    if not devices:
        print("No devices in DB.")
        return

    logs_to_create = []

    for _ in range(num_entries):
        device = random.choice(devices)
        device_types = list(device.device_type.all())

        if not device_types:
            continue

        device_type = random.choice(device_types)

        # ---- RANDOM TIME BETWEEN 2024 & 2025 ----
        random_time = start_date + timedelta(
            seconds=random.randint(0, total_seconds)
        )

        # ---- RANDOM VALUE BASED ON PARAMETER ----
        if 'voltage' in device_type.parameter.lower():
            value = round(random.uniform(200, 240), 2)
        elif 'current' in device_type.parameter.lower():
            value = round(random.uniform(0, 30), 2)
        else:
            value = round(random.uniform(0, 100), 2)

        logs_to_create.append(DeviceLog(
            device=device,
            device_type=device_type,
            time=random_time,
            value=value
        ))

    DeviceLog.objects.bulk_create(logs_to_create)
    print(f"Created {len(logs_to_create)} DeviceLog entries between 2024 and 2025.")

