from django.urls import path
from .views import AnbarModelListView
from . import views 

urlpatterns = [
    path('create_anbar', views.create_anbar, name='create_anbar'),
    path('filter/', AnbarModelListView.as_view(), name='anbar-filter'),
    path('get_all_anbar/', views.get_all_anbar, name='get_all_anbar'),
    path('get_all_anbar/<str:tag>/', views.get_all_anbar, name='get_all_anbar_by_tag'),
]
