from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CityModel
import pandas as pd
import os
import logging
from django.db.models import Q, Count
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.cache import cache_page
from rest_framework.throttling import UserRateThrottle
from datetime import datetime
import io
import openpyxl
from collections import Counter
import jdatetime
from django.db.models import Sum


@api_view(["POST"])
@permission_classes([AllowAny])
def create_tolid(request):
    s_data = request.data
    data_serializers = TolidSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_tolid_by_userID(request, user_id):
    filter_today = request.GET.get("today", "false").lower() == "true"
    user_data = TolidModel.objects.filter(user_id=user_id)

    if filter_today:
        today = jdatetime.date.today()
        user_data = user_data.filter(production_date=today)

    return Response(
        TolidGetSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_full_and_aggregated_tolid_by_user(request, user_id):
    all_tolid = TolidModel.objects.filter(user_id=user_id).select_related("product")

    # لیست جزئیات
    detailed_list = [
        {
            "product_name": item.product.name,
            "production": float(item.production),
            "production_date": (
                str(item.production_date) if item.production_date else None
            ),
        }
        for item in all_tolid
    ]

    # مرتب‌سازی نزولی بر اساس production_date (جدیدترین‌ها اول)
    detailed_list.sort(key=lambda x: x["production_date"] or "", reverse=True)

    # لیست جمع کل
    aggregated = all_tolid.values("product__name").annotate(
        total_production=Sum("production")
    )
    aggregated_list = [
        {
            "product_name": item["product__name"],
            "production": float(item["total_production"]),
        }
        for item in aggregated
    ]

    return Response(
        {"data": detailed_list, "total": aggregated_list}, status=status.HTTP_200_OK
    )
