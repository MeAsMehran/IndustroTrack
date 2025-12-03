from rest_framework import serializers
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField



class CustomUserRegisterSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField(region="IR")

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'username', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
            - hashing the password
            - phone_number : +98 -> 09
        """
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        phone_number = str(instance.phone_number)
        phone_number = phone_number.replace("+98", "0")
        instance.phone_number = phone_number

        instance.save()
        return instance


    


class CustomUserLoginSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField(region="IR")


    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'phone_number', 'email')






