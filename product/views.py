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
from django.db.models import Sum, Count


@api_view(["POST"])
@permission_classes([AllowAny])
def create_product(request):
    s_data = request.data
    data_serializers = ProductSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product(request):
    user_data = ProductModel.objects.all().order_by("-is_active")
    return Response(
        ProductSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product_active(request):
    user_data = ProductModel.objects.filter(is_active=True)
    return Response(
        ProductSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["PATCH"])
@permission_classes([AllowAny])
@transaction.atomic
def edit_product(request, id):
    product = get_object_or_404(ProductModel, id=id)
    serializer = ProductSerializers(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_product_material(request):
    s_data = request.data
    data_serializers = ProductMaterialRelationSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product_material(request):
    product_id = request.GET.get("product_id")

    if product_id:
        user_data = ProductMaterialRelation.objects.filter(product_id=product_id)
    else:
        user_data = ProductMaterialRelation.objects.all()

    # افزودن select_related برای بهینه‌سازی و order_by برای مرتب‌سازی
    user_data = user_data.select_related("material").order_by("material__unit_type")

    return Response(
        ProductMaterialRelationGetSerializers(user_data, many=True).data,
        status=status.HTTP_200_OK,
    )


@api_view(["PATCH"])
@permission_classes([AllowAny])
@transaction.atomic
def edit_product_material(request, id):
    product = get_object_or_404(ProductMaterialRelation, id=id)
    serializer = ProductMaterialRelationSerializers(
        product, data=request.data, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductMaterialsWithWeight(APIView):
    def get(self, request):
        product_id = request.query_params.get("product_id")
        weight = request.query_params.get("weight")

        if not product_id or not weight:
            return Response(
                {"detail": "product_id و weight اجباری هستند."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            weight = float(weight)
        except ValueError:
            return Response(
                {"detail": "مقدار weight باید عددی باشد."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        relations = ProductMaterialRelation.objects.filter(
            product_id=product_id
        ).select_related("material")

        result = []
        for rel in relations:
            total_quantity = rel.quantity_per_unit * weight

            # جستجو در انبار
            anbar_item = AnbarModel.objects.filter(
                name=rel.material.name,
                unit_type=rel.material.unit_type,  # اگر مطمئن نیستی، این شرط رو حذف کن
            ).first()

            # بررسی موجودی
            is_available = False
            current_inventory = 0
            if anbar_item:
                try:
                    current_inventory = float(anbar_item.Inventory)
                    is_available = current_inventory >= total_quantity
                except ValueError:
                    pass  # اگر Inventory عدد نباشد

            result.append(
                {
                    "material_id": rel.material.id,
                    "material_name": rel.material.name,
                    "material_unit_type": rel.material.unit_type,
                    "quantity_per_unit": rel.quantity_per_unit,
                    "total_quantity": total_quantity,
                    "anbar_inventory": current_inventory,
                    "is_available": is_available,
                }
            )

        # مرتب‌سازی بر اساس material_unit_type
        sorted_result = sorted(result, key=lambda x: x["material_unit_type"])

        return Response(sorted_result)


# class ProductMaterialsWithWeight(APIView):
#     def get(self, request):
#         product_id = request.query_params.get("product_id")
#         weight = request.query_params.get("weight")

#         if not product_id or not weight:
#             return Response(
#                 {"detail": "product_id و weight اجباری هستند."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             weight = float(weight)
#         except ValueError:
#             return Response(
#                 {"detail": "مقدار weight باید عددی باشد."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         relations = ProductMaterialRelation.objects.filter(
#             product_id=product_id
#         ).select_related("material")

#         result = []
#         for rel in relations:
#             result.append(
#                 {
#                     "material_id": rel.material.id,
#                     "material_name": rel.material.name,
#                     "material_unit_type": rel.material.unit_type,
#                     "quantity_per_unit": rel.quantity_per_unit,
#                     "total_quantity": rel.quantity_per_unit * weight,
#                 }
#             )

#         # مرتب‌سازی بر اساس material_unit_type
#         sorted_result = sorted(result, key=lambda x: x["material_unit_type"])

#         return Response(sorted_result)


class InventoryAnalysisAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # پارامتر تولید محصول از query string
            X = float(request.query_params.get("amount", 1))

            # تحلیل ۱: بررسی کسری انبار
            shortage_analysis = []
            for rel in ProductMaterialRelation.objects.select_related(
                "product", "material"
            ):
                needed_qty = rel.quantity_per_unit * X
                try:
                    available = float(rel.material.Inventory)
                except ValueError:
                    available = 0.0

                shortage_analysis.append(
                    {
                        "product": rel.product.name,
                        "material": rel.material.name,
                        "needed_quantity": needed_qty,
                        "available": available,
                        "shortage": max(0, needed_qty - available),
                    }
                )

            # تحلیل ۲: سهم هر ماده در محصولات مختلف
            material_stats = (
                ProductMaterialRelation.objects.values("material__name")
                .annotate(
                    num_products=Count("product", distinct=True),
                    total_quantity_used=Sum("quantity_per_unit"),
                )
                .order_by("-num_products")
            )

            material_share = [
                {
                    "material": item["material__name"],
                    "num_products": item["num_products"],
                    "total_quantity_used": item["total_quantity_used"],
                }
                for item in material_stats
            ]

            # تحلیل ۳: مواد اولیه پرمصرف
            most_used = sorted(
                material_share, key=lambda x: x["total_quantity_used"], reverse=True
            )[:10]

            return Response(
                {
                    "shortage_analysis": shortage_analysis,
                    "material_share": material_share,
                    "most_used_materials": most_used,
                }
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ShortageAnalysisAPI(APIView):
    def get(self, request):
        # دریافت مقدار تولید از پارامتر URL، مقدار پیش‌فرض 1
        try:
            amount = float(request.query_params.get("amount", 1))
        except ValueError:
            return Response({"error": "Invalid amount value"}, status=400)

        products = ProductModel.objects.all()
        analysis_data = []

        for product in products:
            product_materials = ProductMaterialRelation.objects.filter(product=product)
            material_data = []

            for material_relation in product_materials:
                material = material_relation.material
                needed_quantity = material_relation.quantity_per_unit * amount
                available = float(material.Inventory)
                shortage = max(needed_quantity - available, 0)

                material_data.append(
                    {
                        "material": material.name,
                        "needed_quantity": round(needed_quantity, 3),
                        "available": round(available, 3),
                        "shortage": round(shortage, 3),
                    }
                )

            analysis_data.append({"product": product.name, "materials": material_data})

        return Response({"amount": amount, "analysis": analysis_data})
