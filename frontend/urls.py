# frontend/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # path("", home, name="home"),
    path("", login_view, name="login"),
    path('dashboard/', dashboard_view, name='dashboard'),

]
