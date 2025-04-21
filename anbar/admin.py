from django.contrib import admin
from .models import *


class AnbarAdmin(admin.ModelAdmin):
    fields = [
        "code",
        "name",
        "barcode",
        "barcode_address",
        "iran_code",
        "description",
        "Inventory",
        "min_Inventory",
        "max_Inventory",
        "unit_type",
        "sub_unit_type",
        "tag",
    ]
    list_display = ["name", "code", "min_Inventory", "tag"]
    list_filter = ["name"]
    search_fields = ["name", "code"]


admin.site.register(AnbarModel, AnbarAdmin)
