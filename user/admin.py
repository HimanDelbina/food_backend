from django.contrib import admin
from .models import *

# Register your models here.


class UnitAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class WorkTypeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class PostWorkAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class OstanAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


class CityAdmin(admin.ModelAdmin):
    fields = ["name", "ostan"]
    list_display = ["name", "ostan"]
    list_filter = ["name"]
    search_fields = ["name"]


class ChildAdmin(admin.ModelAdmin):
    fields = ["name", "birthday", "gender"]
    list_display = ["name", "birthday", "gender"]
    list_filter = ["name"]
    search_fields = ["name"]


class PersonelAdmin(admin.ModelAdmin):
    fields = [
        "person_code",
        "password",
        "first_name",
        "last_name",
        "date_employ",
        "unit",
        "work_type",
        "post_work",
        "shift",
        "is_online",
        "is_active",
        "phone_number",
        "melli_code",
        "sh_code",
        "sh_s_code",
        "father_name",
        "birthday",
        "sh_ostan",
        "burn_ostan",
        "gender",
        "solder_select",
        "reason_ex",
        "education",
        "education_field",
        "univercity",
        "Institute",
        "ev_file",
        "is_marid",
        "wife_name",
        "wife_birthday",
        "child_count",
        "boy_child_count",
        "girl_child_count",
        "child",
        "insurance_number",
        "insurance_history_day",
        "insurance_history_year",
        "bank_number",
        "bank_shaba",
        "address",
        "post_code",
        "settlement_date",
        "settlement_description",
        "settlement_steps",
        "issue_date",
        "married_date",
        "access",
    ]
    list_display = [
        "person_code",
        "first_name",
        "last_name",
        "is_online",
        "is_active",
        "access",
    ]
    list_filter = ["is_online", "gender"]
    search_fields = ["first_name", "last_name", "person_code"]


admin.site.register(UnitModel, UnitAdmin)
admin.site.register(OstanModel, OstanAdmin)
admin.site.register(CityModel, CityAdmin)
admin.site.register(ChildModel, ChildAdmin)
admin.site.register(PersonelModel, PersonelAdmin)
admin.site.register(WorkTypeModel, WorkTypeAdmin)
admin.site.register(PostWorkModel, PostWorkAdmin)
