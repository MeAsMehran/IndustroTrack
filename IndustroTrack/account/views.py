# drf:
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

# models:
from .models import CustomUser

# Tokens:
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# permissions:
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions.is_super_user import IsSuperUser

# Serializers:
from .serializers import CustomUserRegisterSerializer, CustomUserLoginSerializer, UserSerializer, CustomUserLogoutSerializer


# Create your views here.

class UserRegisterAPIView(APIView):
    
    serializer_class = CustomUserRegisterSerializer

    @swagger_auto_schema(request_body=CustomUserRegisterSerializer)
    def post(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    serializer_class = CustomUserLoginSerializer

    @swagger_auto_schema(request_body=CustomUserLoginSerializer)
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # This will invalidate the token
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class UserListsView(ListAPIView):
    permission_class = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

