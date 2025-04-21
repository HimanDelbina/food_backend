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

