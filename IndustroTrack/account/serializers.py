from rest_framework import serializers
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password


from account.validations.validate_user_register import validate_register
class CustomUserRegisterSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField(region="IR",)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'username', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        return validate_register(data)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user


from account.validations.validate_user_login import validate_login
class CustomUserLoginSerializer(serializers.Serializer):
    """
        For Serializing the User Login
    """
    phone_number = PhoneNumberField(region="IR")
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.DictField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['phone_number']
        
    def validate(self, data):
        return validate_login(data)


class CustomUserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'phone_number', 'email')






