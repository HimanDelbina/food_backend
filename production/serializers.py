from rest_framework import serializers
from .models import *
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField


class TolidSerializers(serializers.ModelSerializer):
    expiration_date = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )
    production_date = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )

    class Meta:
        model = TolidModel
        fields = "__all__"


class AnbarTolidSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnbarTolidModel
        fields = "__all__"


class AnbarGhSerializers(serializers.ModelSerializer):
    start_date = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )
    end_date = JDateTimeField(format="%Y/%m/%d %H:%M", required=False, allow_null=True)

    class Meta:
        model = AnbarGhModel
        fields = "__all__"


class AnbarExitSerializers(serializers.ModelSerializer):
    exit_date = JDateTimeField(format="%Y/%m/%d %H:%M", required=False, allow_null=True)

    class Meta:
        model = AnbarExitModel
        fields = "__all__"
