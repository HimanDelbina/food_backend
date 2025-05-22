from django.urls import path
from . import views
from user.views import *

urlpatterns = [
    path("create_person", views.create_person, name="create_person"),
    path("get_all_person", views.get_all_person, name="get_all_person"),
    path("get_flter_person/", views.get_flter_person, name="get_flter_person"),
    path("change_password", ChangePasswordView.as_view(), name="change_password"),
    path("edit_user/<int:id>", views.edit_user, name="edit_user"),
    path("login_view", views.login_view, name="login_view"),
    path("signup_view", views.signup_view, name="signup_view"),
    path("get_user_data", GetUserDataView.as_view(), name="get_user_data"),
    ####################################################################
    path("get_unit", views.get_unit, name="get_unit"),
    path("get_postWork", views.get_postWork, name="get_postWork"),
    path("get_workType", views.get_workType, name="get_workType"),
    path("edit_unit/<int:id>", views.edit_unit, name="edit_unit"),
    path("edit_postwork/<int:id>", views.edit_postwork, name="edit_postwork"),
    path("edit_worktype/<int:id>", views.edit_worktype, name="edit_worktype"),
    ####################################################################
    path("get_ostan", views.get_ostan, name="get_ostan"),
    path("get_shahrestan", views.get_shahrestan, name="get_shahrestan"),
    path(
        "get_shahrestan_by_ostanID/<int:ostan_id>",
        views.get_shahrestan_by_ostanID,
        name="get_shahrestan_by_ostanID",
    ),
    # path("delete_all_cities", views.delete_all_cities, name="delete_all_cities"),
    ####################################################################
    path("get_child", views.get_child, name="get_child"),
    ####################################################################
    path("add_ostans", AddOstansFromExcel.as_view(), name="add_ostans"),
    path("add_city", AddCitiesFromExcel.as_view(), name="add_city"),
    path("download_users_excel", download_users_excel, name="download_users_excel"),
    path(
        "check_active/<str:person_code>/",
        views.get_user_active_status,
        name="check_user_active_status",
    ),
    #################################################################### Destination
    path("create_destination", create_destination, name="create_destination"),
    path("get_all_destination", get_all_destination, name="get_all_destination"),
    path("edit_destination/<int:id>", edit_destination, name="edit_destination"),
    path(
        "delete_anbar_request/<int:id>",
        delete_anbar_request,
        name="delete_anbar_request",
    ),
]
