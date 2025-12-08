from rest_framework.exceptions import ValidationError
from rest_framework.views import status
from account.models import CustomUser


def validate_register(data):

    # Formatting the phone_number
    phone_number = str(data.get('phone_number')) 

    if phone_number.startswith("+98"): phone_number = phone_number.replace("+98", "0")
    elif not phone_number.startswith("+98") and not phone_number.startswith("0"):
        phone_number = "0" + phone_number

    data["phone_number"] = phone_number

    password = data.get('password')
    
    # phone number length 

    if phone_number is not None:
        user = CustomUser.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError({'phone_number' : "The Phone Number is registered!"})
    elif phone_number is "0":
        raise ValidationError("Enter a Phone Number!", status.HTTP_400_BAD_REQUEST)

    if password is None:    # serializer required
        raise ValidationError("Enter a password!", status.HTTP_400_BAD_REQUEST)

    return data


# def check_password():


