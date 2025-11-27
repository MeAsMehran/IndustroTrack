from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class CustomUser(AbstractUser):

    phone_number = PhoneNumberField()
    password = models.CharField(max_length=20, null=False)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=True, max_length=255)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.phone_number


