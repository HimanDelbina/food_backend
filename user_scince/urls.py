from django.urls import path
from user import views
from .views import *

urlpatterns = [
    path("age_distribution", PersonelAnalysisView.as_view(), name="age_distribution"),
]
