from django.urls import path
from . import views
from production.views import *

urlpatterns = [
    path("create_tolid", views.create_tolid, name="create_tolid"),
]
