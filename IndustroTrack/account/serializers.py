from rest_framework import serializers
from .models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomUserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}



