from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class CustomUser(AbstractUser):

    # phone_number = models.CharField(max_length=11, unique=True, )
    phone_number = PhoneNumberField(unique=True)
    password = models.CharField(max_length=128, null=False)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=True, max_length=255)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return str(self.phone_number)


