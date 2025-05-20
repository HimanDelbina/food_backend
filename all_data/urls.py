from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path(
        "get_all_requests_by_type/",
        views.get_all_requests_by_type,
        name="get_all_requests_by_type",
    ),
]
