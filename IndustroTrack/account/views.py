from http.cookiejar import Cookie
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import CustomUserRegisterSerializer, CustomUserLoginSerializer, UserSerializer
from rest_framework.response import Response
from .models import CustomUser
import jwt, datetime
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class UserRegisterAPIView(APIView):
    serializer_class = CustomUserRegisterSerializer


    @swagger_auto_schema(request_body=CustomUserRegisterSerializer)
    def post(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        
        # Access Token 
        access_payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        # CREATING THE ACCESS_TOKEN:
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        access_token = jwt.encode(access_payload, 'secret', algorithm='HS256')

        # Refresh Token 
        refresh_payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
        }

        # CREATING THE REFRESH_TOKEN:
        refresh_token = jwt.encode(refresh_payload, 'secret', algorithm='HS256')

        # MAKING A COOKIE
        response = Response()
        response.set_cookie(key='jwt', value=access_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return {
            'response' : response,
            'status' : 200
        }


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

    def post(self,request):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'Successfully logged out',
        }
        return response


class UserListsView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

