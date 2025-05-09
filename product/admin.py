from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "unit", "is_active"]
    list_display = ["name", "unit", "is_active"]
    list_filter = ["name", "is_active"]
    search_fields = ["name"]


class ProductMaterialRelationAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.name

    def material_name(self, obj):
        return obj.material.name

    fields = ["product", "material", "quantity_per_unit"]
    list_display = ["product_name", "material_name", "quantity_per_unit"]


admin.site.register(ProductModel, ProductAdmin)
admin.site.register(ProductMaterialRelation, ProductMaterialRelationAdmin)
