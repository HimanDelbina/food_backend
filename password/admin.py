from django.contrib import admin
from .models import *


# Register your models here.
class PasswordItemAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.user.first_name

    fields = ["user", "title", "username", "password", "note"]
    list_display = ["product_name", "title", "username", "password", "note"]


admin.site.register(PasswordItem, PasswordItemAdmin)
