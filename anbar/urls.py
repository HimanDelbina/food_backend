from django.urls import path
from .views import AnbarModelListView
from . import views 

urlpatterns = [
    path('create_anbar', views.create_anbar, name='create_anbar'),
    path('filter/', AnbarModelListView.as_view(), name='anbar-filter'),
    path('get_all_anbar/', views.get_all_anbar, name='get_all_anbar'),
    path('get_all_anbar/<str:tag>/', views.get_all_anbar, name='get_all_anbar_by_tag'),
    path("get_shopgroupe", views.get_shopgroupe, name="get_shopgroupe"),
    path("get_sellgroupe", views.get_sellgroupe, name="get_sellgroupe"),
    path("get_kalagroupe", views.get_kalagroupe, name="get_kalagroupe"),
]
