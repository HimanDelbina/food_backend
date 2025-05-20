from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("create_anbar", views.create_anbar, name="create_anbar"),
    path("get_all_kala", views.get_all_kala, name="get_all_kala"),
    path("get_complete_request", views.get_complete_request, name="get_complete_request"),
    path("filter/", AnbarModelListView.as_view(), name="anbar-filter"),
    path("get_all_anbar/", views.get_all_anbar, name="get_all_anbar"),
    path("get_all_anbar/<str:tag>/", views.get_all_anbar, name="get_all_anbar_by_tag"),
    path(
        "get_request_anbar_for_anbar",
        views.get_request_anbar_for_anbar,
        name="get_request_anbar_for_anbar",
    ),
    path(
        "edit_request_anbar/<int:id>",
        views.edit_request_anbar,
        name="edit_request_anbar",
    ),
    #########################################################
    path("create_request", views.create_request, name="create_request"),
    path("get_all_request", views.get_all_request, name="get_all_request"),
    path(
        "delete_anbar_request/<int:request_id>",
        views.delete_anbar_request,
        name="delete_anbar_request",
    ),
    path(
        "get_request_userID/<int:user_id>",
        views.get_request_userID,
        name="get_request_userID",
    ),
    path("anbar_ai", AnbarRequestAIAPIView.as_view(), name="anbar_ai"),
    path("anbar_analytics", AnbarAnalyticsAPIView.as_view(), name="anbar_analytics"),
    path("approve_request", approve_request_api, name="approve_request"),
    path("undo_request", undo_request_api, name="undo_request"),
]
