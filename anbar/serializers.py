from rest_framework import serializers
from .models import *
from user.serializers import *


class AnbarSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnbarModel
        fields = "__all__"


class AnbarGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnbarModel
        fields = "__all__"
        depth = 1


# class AnbarRequestSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = AnbarRequestModel
#         fields = "__all__"
class AnbarRequestSerializers(serializers.ModelSerializer):
    kala = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = AnbarRequestModel
        fields = ["user", "kala", "description"]

    def create(self, validated_data):
        user = validated_data["user"]
        kala_data = validated_data["kala"]
        final_kala_list = []

        for item in kala_data:
            kala_id = item.get("kala_id")
            quantity = item.get("quantity")

            try:
                anbar_item = AnbarModel.objects.get(id=kala_id)
            except AnbarModel.DoesNotExist:
                raise serializers.ValidationError(
                    {"kala": f"کالایی با ID {kala_id} یافت نشد."}
                )

            final_kala_list.append(
                {
                    "id": anbar_item.id,
                    "code": anbar_item.code,
                    "product_name": anbar_item.name,
                    "iran_code": anbar_item.iran_code,
                    "unit_type": anbar_item.unit_type,
                    "weight": quantity,
                }
            )

        return AnbarRequestModel.objects.create(
            user=user,
            kala=final_kala_list,
            description=validated_data.get("description", ""),
        )


class AnbarRequestGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnbarRequestModel
        fields = "__all__"
        depth = 1


class AnbarRequestGetSerializers(serializers.ModelSerializer):
    kala_details = serializers.SerializerMethodField()
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = AnbarRequestModel
        fields = "__all__"  # یا دقیق‌تر اگه خواستی
        # fields = ['id', 'user', 'description', 'status', 'kala_details', 'create_at', 'user_first_name', 'user_last_name']

    def get_kala_details(self, obj):
        return obj.get_kala_details()
