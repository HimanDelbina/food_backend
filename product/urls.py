from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("create_product", views.create_product, name="create_product"),
    path("get_product", views.get_product, name="get_product"),
    path("get_product_active", views.get_product_active, name="get_product_active"),
    path("edit_product/<int:id>", views.edit_product, name="edit_product"),
    path(
        "create_product_material",
        views.create_product_material,
        name="create_product_material",
    ),
    path(
        "edit_product_material/<int:id>",
        views.edit_product_material,
        name="edit_product_material",
    ),
    path(
        "get_product_material/", views.get_product_material, name="get_product_material"
    ),
    path(
        "product_materials_calculator/",
        ProductMaterialsWithWeight.as_view(),
        name="product_materials_calculator",
    ),
    path(
        "inventory_analysis",
        InventoryAnalysisAPIView.as_view(),
        name="inventory_analysis",
    ),
    path("shortage_analysis/", ShortageAnalysisAPI.as_view(), name="shortage_analysis"),
]
