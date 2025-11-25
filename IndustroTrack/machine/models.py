from django.db import models

# Create your models here.


CHOICES = (
    ('voltage', 'Voltage'),
    ('current', 'Current'),
    ('power', 'Power'),
    ('temperature', 'Temperature'),
    ('water', 'Water'),
    ('electric', 'Electric'),
    ('gas', 'Gas'),
    ('other', 'Other'),
)


class DeviceType(models.Model):

    # device = models.ForeignKey(Device, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=100, )
    code = models.IntegerField()
    des = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.parameter}"


class Device(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField()
    des = models.CharField(max_length=250, blank=True, null=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class DeviceLog(models.Model):

    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()