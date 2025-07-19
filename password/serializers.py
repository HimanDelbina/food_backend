from rest_framework import serializers
from .models import PasswordItem
from user.models import *


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelModel
        fields = ["id", "first_name", "last_name"]


class PasswordItemSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = PasswordItem
        fields = '__all__'
        read_only_fields = ['user']