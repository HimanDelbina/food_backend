from django.contrib import admin
from .models import *

# Register your models here.


class ShopGroupAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class SellGroupAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class KalaGroupAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class AnbarAdmin(admin.ModelAdmin):
    fields = [
        "code",
        "name",
        "barcode",
        "barcode_address",
        "iran_code",
        "description",
        "shop_group",
        "sell_groupe",
        "kala_group",
        "Inventory",
        "min_Inventory",
        "max_Inventory",
        "unit_type",
        "sub_unit_type",
        "tag",
    ]
    list_display = ["name", "code", "min_Inventory","tag"]
    list_filter = ["name"]
    search_fields = ["name", "code"]


admin.site.register(ShopGroupModel, ShopGroupAdmin)
admin.site.register(SellGroupModel, SellGroupAdmin)
admin.site.register(KalaGroupModel, KalaGroupAdmin)
admin.site.register(AnbarModel, AnbarAdmin)
