from django.urls import path

from .views import CreateDevice

urlpatterns = [

    path('create/', CreateDevice.as_view(), name='create-machine'),


]