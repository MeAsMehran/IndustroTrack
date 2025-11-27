from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from .models import CustomUser

# Create your views here.

class UserRegisterAPIView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password!')

        return Response({'message': 'Login Success!'})




