from rest_framework import serializers
from .models import CustomUser
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken



class CustomUserRegisterSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField(region="IR")
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'username', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
            - hashing the password
            - phone_number : 
                - +98 -> +98 -> 0
                - 0 -> +98 -> 0 
                - ... -> +98 -> 0
        """
        instance = self.Meta.model(**validated_data)    # or instance = CustomUser(**validated_data)

        password = validated_data.pop('password')
        if password is not None:
            instance.set_password(password)

        phone_number_value = str(instance.phone_number).replace("+98", "0")
        instance.phone_number = phone_number_value

        instance.save()
        return instance


class CustomUserLoginSerializer(serializers.Serializer):

    phone_number = PhoneNumberField(region="IR")
    password = serializers.CharField(write_only=True, required=True)
    refresh = serializers.CharField(read_only=True)     # Only reason to set it here is when we call the serializers.data in Response, it only return the field here
    access = serializers.CharField(read_only=True)      # Only reason to set it here is when we call the serializers.data in Response, it only return the field here

    def validate(self, data):
        phone_number_value = str(data['phone_number']).replace('+98', '0')
        password_value = data['password']

        user = CustomUser.objects.filter(phone_number=phone_number_value).first()

        if not user:
            raise AuthenticationFailed('user not found!')
        
        if not user.check_password(password_value):
            raise AuthenticationFailed('Invalid password!')
        
        refresh = RefreshToken.for_user(user)

        return {
            'phone_number': phone_number_value,
            'password': password_value,
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'phone_number', 'email')






