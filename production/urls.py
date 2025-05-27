from django.urls import path
from . import views
from production.views import *

urlpatterns = [
    path("create_tolid", views.create_tolid, name="create_tolid"),
    path(
        "get_tolid_by_userID/<int:user_id>",
        views.get_tolid_by_userID,
        name="get_tolid_by_userID",
    ),
    path(
        "get_full_and_aggregated_tolid_by_user/<int:user_id>/",
        views.get_full_and_aggregated_tolid_by_user,
        name="get_full_and_aggregated_tolid_by_user",
    ),
]
