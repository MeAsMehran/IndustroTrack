from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import CustomUserRegisterSerializer, CustomUserLoginSerializer
from rest_framework.response import Response
from .models import CustomUser
import jwt, datetime

# Create your views here.

class UserRegisterAPIView(APIView):
    serializer_class = CustomUserRegisterSerializer

    @swagger_auto_schema(request_body=CustomUserRegisterSerializer)
    def post(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    serializer_class = CustomUserLoginSerializer

    @swagger_auto_schema(request_body=CustomUserLoginSerializer)
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        # CREATING THE TOKEN:
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # MAKING A COOKIE
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token,
        }

        return response


class UserView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserLoginSerializer(user)


        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'Successfully logged out',
        }
        return response




