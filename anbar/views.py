from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.decorators import permission_classes, api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import os
import logging
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import AnbarModel
from .serializers import AnbarGetSerializers
from .filters import AnbarModelFilter
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Cast
from user.models import *
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions  # Ensure permissions is imported


@api_view(["POST"])
@permission_classes([AllowAny])
def create_anbar(request):
    s_data = request.data
    print(request.data)
    data_serializers = AnbarSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_anbar(request, tag=None):
    # دریافت داده‌ها از مدل
    kala_data = AnbarModel.objects.all()
    if tag:
        kala_data = kala_data.filter(tag=tag)
    response_data = {
        "total_kala": kala_data.count(),
        "kala": AnbarGetSerializers(kala_data, many=True).data,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_kala(request):
    user_data = AnbarModel.objects.all()
    return Response(
        AnbarGetSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_request(request):
    user_data = AnbarRequestModel.objects.all()
    return Response(
        AnbarRequestGetSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_request_userID(request, user_id):
    data = AnbarRequestModel.objects.filter(user_id=user_id)
    serializer = AnbarRequestGetSerializers(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AnbarModelListView(generics.ListAPIView):
    queryset = AnbarModel.objects.all()
    serializer_class = AnbarGetSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnbarModelFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        inventory_status = self.request.query_params.get("inventory_status")
        # Convert CharFields to float for comparison
        inventory_float = ExpressionWrapper(
            Cast(F("Inventory"), FloatField()), output_field=FloatField()
        )
        min_inventory_float = ExpressionWrapper(
            Cast(F("min_Inventory"), FloatField()), output_field=FloatField()
        )
        max_inventory_float = ExpressionWrapper(
            Cast(F("max_Inventory"), FloatField()), output_field=FloatField()
        )
        if inventory_status == "less":
            queryset = queryset.annotate(
                inventory_f=inventory_float, min_inventory_f=min_inventory_float
            ).filter(inventory_f__lt=F("min_inventory_f"))
        elif inventory_status == "greater":
            queryset = queryset.annotate(
                inventory_f=inventory_float, max_inventory_f=max_inventory_float
            ).filter(inventory_f__gt=F("max_inventory_f"))
        elif inventory_status == "min_greater":
            queryset = queryset.annotate(
                inventory_f=inventory_float, min_inventory_f=min_inventory_float
            ).filter(inventory_f__gt=F("min_inventory_f"))
        return queryset


@api_view(["POST"])
@permission_classes([AllowAny])
def create_request(request):
    s_data = request.data
    print(request.data)
    data_serializers = AnbarRequestSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AnbarRequestAIAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        kala_list = request.data.get("kala", [])
        user = get_object_or_404(PersonelModel, id=user_id)
        final_kala_list = []
        for item in kala_list:
            name = item.get("product_name")
            weight = item.get("weight")
            try:
                # جستجو فقط با استفاده از نام کالا
                anbar_item = AnbarModel.objects.get(name=name)
            except AnbarModel.DoesNotExist:
                return Response(
                    {"error": f"کالا با نام {name} پیدا نشد."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            final_kala_list.append(
                {
                    "id": anbar_item.id,
                    "code": anbar_item.code,
                    "product_name": anbar_item.name,
                    "iran_code": anbar_item.iran_code,
                    "unit_type": anbar_item.unit_type,
                    "weight": weight,
                }
            )
        AnbarRequestModel.objects.create(
            user=user,
            kala=final_kala_list,
            description=request.data.get("description", ""),
        )
        return Response(
            {"message": "درخواست انبار با موفقیت ثبت شد."},
            status=status.HTTP_201_CREATED,
        )


@api_view(["DELETE"])
def delete_anbar_request(request, request_id):
    try:
        anbar_request = AnbarRequestModel.objects.get(id=request_id)
    except AnbarRequestModel.DoesNotExist:
        return Response({"error": "درخواست مورد نظر پیدا نشد."}, status=404)

    anbar_request.delete()
    return Response({"message": "درخواست با موفقیت حذف شد."}, status=204)
