from django.contrib import admin
from .models import *

# Register your models here.


class TolidAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        return obj.user.first_name

    def product_name(self, obj):
        return obj.product.name

    fields = [
        "user",
        "product",
        "production",
        "batch_number",
        "is_export",
        "description",
        "expiration_date",
        "production_date",
    ]
    list_display = [
        "user_name",
        "product_name",
        "production",
        "batch_number",
        "is_export",
    ]
    list_filter = ["is_export"]
    search_fields = ["user_name"]


class AnbarTolidAdmin(admin.ModelAdmin):

    fields = [
        "tolid_item",
        "total_inventory",
        "remaining_inventory",
    ]
    list_display = [
        "total_inventory",
        "remaining_inventory",
    ]


class AnbarExitAdmin(admin.ModelAdmin):
    def destination_name(self, obj):
        return obj.destination.first_name

    fields = [
        "anbar_item",
        "amount",
        "destination",
        "description",
        "exit_date",
    ]
    list_display = [
        "destination_name",
        "amount",
        "exit_date",
    ]


admin.site.register(TolidModel, TolidAdmin)
admin.site.register(AnbarTolidModel, AnbarTolidAdmin)
admin.site.register(AnbarExitModel, AnbarExitAdmin)
