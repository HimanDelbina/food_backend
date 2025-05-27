from rest_framework import serializers
from .models import *


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"


class FixedCostSerializers(serializers.ModelSerializer):
    class Meta:
        model = FixedCostModel
        fields = "__all__"


class ProductMaterialRelationSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterialRelation
        fields = "__all__"


class ProductMaterialRelationGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterialRelation
        fields = "__all__"
        depth = 1
