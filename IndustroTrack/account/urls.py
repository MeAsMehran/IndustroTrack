from django.urls import path

from .views import UserRegisterAPIView, UserLoginAPIView

app_name='machine'

urlpatterns = [

    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),

]
