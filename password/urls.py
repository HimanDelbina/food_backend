from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("get_passwords", views.get_passwords, name="get_passwords"),
]
