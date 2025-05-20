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
    list_display = ["name", "code", "Inventory","min_Inventory","max_Inventory","tag"]
    list_filter = ["name"]
    search_fields = ["name", "code"]


class AnbarRequestAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "kala",
        "description",
        "status",
        "approved_by",
        "approved_at",
    ]
    list_display = ["kala", "status"]
    list_filter = ["status"]


admin.site.register(AnbarModel, AnbarAdmin)
admin.site.register(AnbarRequestModel, AnbarRequestAdmin)
