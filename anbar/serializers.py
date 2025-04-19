from rest_framework import serializers
from .models import *


class AnbarSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnbarModel
        fields = "__all__"
class AnbarGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnbarModel
        fields = "__all__"
        depth=1


class ShopGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShopGroupModel
        fields = "__all__"


class SellGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = SellGroupModel
        fields = "__all__"


class KalaGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = KalaGroupModel
        fields = "__all__"
