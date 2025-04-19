from rest_framework import serializers
from .models import *
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField


class PostWorkSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostWorkModel
        fields = "__all__"


class WorkTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = WorkTypeModel
        fields = "__all__"


class UnitSerializers(serializers.ModelSerializer):
    class Meta:
        model = UnitModel
        fields = "__all__"


class OstanSerializers(serializers.ModelSerializer):
    class Meta:
        model = OstanModel
        fields = "__all__"


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = "__all__"
        depth = 1


class CitySimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = "__all__"


class ChildSerializers(serializers.ModelSerializer):
    birthday = JDateTimeField(format="%Y/%m/%d %H:%M", required=False, allow_null=True)

    class Meta:
        model = ChildModel
        fields = "__all__"


class PersonSerializers(serializers.ModelSerializer):
    date_employ = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )
    birthday = JDateTimeField(format="%Y/%m/%d %H:%M", required=False, allow_null=True)
    wife_birthday = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )
    settlement_date = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )

    create_at = JDateTimeField(format="%Y/%m/%d %H:%M", required=False)
    update_at = JDateTimeField(format="%Y/%m/%d %H:%M", required=False)

    class Meta:
        model = PersonelModel
        fields = "__all__"


class PersonGetSerializers(serializers.ModelSerializer):
    date_employ = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )
    birthday = JDateTimeField(format="%Y/%m/%d %H:%M", required=False, allow_null=True)
    wife_birthday = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )
    settlement_date = JDateTimeField(
        format="%Y/%m/%d %H:%M", required=False, allow_null=True
    )

    create_at = JDateTimeField(format="%Y/%m/%d %H:%M", required=False)
    update_at = JDateTimeField(format="%Y/%m/%d %H:%M", required=False)

    class Meta:
        model = PersonelModel
        fields = "__all__"
        depth = 1


class ChangePasswordSerializer(serializers.Serializer):
    person_code = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        person_code = data.get("person_code")
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        try:
            person = PersonelModel.objects.get(person_code=person_code)
        except PersonelModel.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "person_code": {
                        "message": "کاربری با این شماره پرسنلی وجود ندارد.",
                        "status": 404,
                    }
                }
            )

        if person.password != current_password:
            raise serializers.ValidationError(
                {
                    "current_password": {
                        "message": "رمز عبور فعلی اشتباه است.",
                        "status": 401,
                    }
                }
            )

        if person.password == new_password:
            raise serializers.ValidationError(
                {
                    "new_password": {
                        "message": "رمز عبور جدید نباید با رمز فعلی یکسان باشد.",
                        "status": 409,
                    }
                }
            )

        return data


class LoginSerializer(serializers.Serializer):
    person_code = serializers.CharField()
    password = serializers.CharField()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelModel
        fields = "__all__"

    def validate_person_code(self, value):
        if PersonelModel.objects.filter(person_code=value).exists():
            raise serializers.ValidationError("شماره پرسنلی قبلاً ثبت شده است.")
        return value
