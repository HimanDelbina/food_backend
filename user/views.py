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
from .models import CityModel
import pandas as pd
import os
import logging
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets


@api_view(["POST"])
@permission_classes([AllowAny])
def create_person(request):
    s_data = request.data
    print(request.data)
    data_serializers = PersonSerializers(data=s_data)
    if data_serializers.is_valid():
        data_serializers.save()
        return Response(data_serializers.data, status=status.HTTP_201_CREATED)
    return Response(data_serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_person(request):
    # دریافت داده‌ها از مدل
    user_data = PersonelModel.objects.all()

    # شمارش تعداد کاربران بر اساس وضعیت is_online
    active_users = user_data.filter(is_online="A").count()
    mission_users = user_data.filter(is_online="MA").count()
    consultation_users = user_data.filter(is_online="MO").count()

    # ایجاد داده‌ها برای ارسال در پاسخ
    response_data = {
        "total_users": user_data.count(),  # تعداد کل کاربران
        "active_users": active_users,  # تعداد کاربران فعال
        "mission_users": mission_users,  # تعداد کاربران مامور
        "consultation_users": consultation_users,  # تعداد کاربران مشاوره
        "users": PersonGetSerializers(user_data, many=True).data,  # لیست کامل کاربران
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_postWork(request):
    user_data = PostWorkModel.objects.all()
    return Response(
        PostWorkSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_workType(request):
    user_data = WorkTypeModel.objects.all()
    return Response(
        WorkTypeSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_unit(request):
    user_data = UnitModel.objects.all()
    return Response(
        UnitSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_ostan(request):
    user_data = OstanModel.objects.all()
    return Response(
        OstanSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_shahrestan(request):
    user_data = CityModel.objects.all()
    return Response(
        CitySimpleSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_shahrestan_by_ostanID(request, ostan_id):
    user_data = CityModel.objects.filter(ostan_id=ostan_id)
    return Response(
        CitySimpleSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_child(request):
    user_data = ChildModel.objects.all()
    return Response(
        ChildSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@csrf_exempt
def delete_all_cities(request):
    if request.method == "DELETE":
        CityModel.objects.all().delete()
        return JsonResponse({"message": "تمام داده‌های شهرستان حذف شدند."}, status=200)
    return JsonResponse({"error": "متد غیرمجاز"}, status=405)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_flter_person(request):
    queryset = PersonelModel.objects.all()

    # گرفتن فیلترها از query params
    gender = request.GET.get("gender")
    is_online = request.GET.get("is_online")
    shift = request.GET.get("shift")
    person_code = request.GET.get("person_code")
    date_employ = request.GET.get("date_employ")  # تاریخ دقیق
    date_employ__gte = request.GET.get("date_employ__gte")
    date_employ__lte = request.GET.get("date_employ__lte")
    unit = request.GET.get("unit")
    work_type = request.GET.get("work_type")
    post_work = request.GET.get("post_work")
    solder_select = request.GET.get("solder_select")
    child_count = request.GET.get("child_count")

    if gender:
        queryset = queryset.filter(gender=gender)
    if is_online:
        queryset = queryset.filter(is_online=is_online)
    if shift:
        queryset = queryset.filter(shift=shift)
    if person_code:
        queryset = queryset.filter(person_code=person_code)
    if unit:
        queryset = queryset.filter(unit_id=unit)
    if work_type:
        queryset = queryset.filter(work_type_id=work_type)
    if post_work:
        queryset = queryset.filter(post_work_id=post_work)
    if solder_select:
        queryset = queryset.filter(solder_select=solder_select)
    if child_count:
        queryset = queryset.filter(child_count=child_count)

    # فیلتر تاریخ استخدام (تبدیل به فرمت میلادی اگر از جلالی می‌فرستی)
    try:
        if date_employ:
            queryset = queryset.filter(date_employ=date_employ)
        if date_employ__gte:
            queryset = queryset.filter(date_employ__gte=date_employ__gte)
        if date_employ__lte:
            queryset = queryset.filter(date_employ__lte=date_employ__lte)
    except Exception as e:
        print(f"خطا در فیلتر تاریخ: {e}")

    serialized_data = PersonGetSerializers(queryset, many=True).data
    return Response(serialized_data, status=status.HTTP_200_OK)


class AddOstansFromExcel(APIView):
    def post(self, request, *args, **kwargs):
        # مسیر فایل اکسل
        file_path = (
            "C:/Users/it/Desktop/Django/ostan.xlsx"  # مسیر فایل را اینجا مشخص کنید
        )

        try:
            # خواندن فایل اکسل
            df = pd.read_excel(file_path)

            # حذف فضای خالی اضافی از نام استان‌ها
            df["ostan"] = df["ostan"].str.strip()

            # اضافه کردن داده‌ها به مدل
            added_count = 0
            for index, row in df.iterrows():
                ostan_name = row["ostan"]
                if not OstanModel.objects.filter(name=ostan_name).exists():
                    OstanModel.objects.create(name=ostan_name)
                    added_count += 1

            return Response(
                {"message": f"{added_count} استان با موفقیت اضافه شد."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddCitiesFromExcel(APIView):
    def post(self, request, *args, **kwargs):
        # مسیر فایل اکسل
        file_path = (
            "C:/Users/it/Desktop/Django/shahr.xlsx"  # مسیر فایل را اینجا مشخص کنید
        )

        try:
            # خواندن فایل اکسل
            df = pd.read_excel(file_path)

            # حذف فضای خالی اضافی از نام شهرها
            df["City"] = df["City"].str.strip()

            # اضافه کردن داده‌ها به مدل CityModel
            added_count = 0
            for index, row in df.iterrows():
                state_id = row["State"]  # شناسه استان
                city_name = row["City"]  # نام شهر

                try:
                    # پیدا کردن استان مرتبط با شناسه
                    ostan = OstanModel.objects.get(id=state_id)

                    # بررسی تکراری بودن شهر
                    if not CityModel.objects.filter(
                        name=city_name, ostan=ostan
                    ).exists():
                        CityModel.objects.create(ostan=ostan, name=city_name)
                        added_count += 1
                        print(f"شهر {city_name} به استان {ostan.name} اضافه شد.")
                    else:
                        print(f"شهر {city_name} قبلاً وجود دارد.")

                except OstanModel.DoesNotExist:
                    return Response(
                        {"error": f"استان با شناسه {state_id} وجود ندارد."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            return Response(
                {"message": f"{added_count} شهر با موفقیت اضافه شد."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            person_code = serializer.validated_data["person_code"]
            new_password = serializer.validated_data["new_password"]

            person = PersonelModel.objects.get(person_code=person_code)
            person.password = new_password
            person.save()

            return Response(
                {"status": True, "message": "رمز عبور با موفقیت تغییر کرد."},
                status=status.HTTP_200_OK,
            )

        # دریافت اولین خطا و تعیین status
        errors = serializer.errors
        first_error_field = list(errors.keys())[0]
        first_error = errors[first_error_field]

        # اگه پیام به صورت dict بود، status رو ازش استخراج می‌کنیم
        custom_status = 400
        if isinstance(first_error, dict):
            message = first_error.get("message", "خطای نامشخص")
            custom_status = first_error.get("status", 400)
        else:
            message = first_error[0]

        return Response(
            {"status": False, "field": first_error_field, "message": message},
            status=custom_status,
        )


@api_view(["PATCH"])
@permission_classes([AllowAny])
def edit_user(request, id):
    try:
        person = PersonelModel.objects.get(person_code=id)
    except PersonelModel.DoesNotExist:
        return Response({"error": "کاربر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PersonSerializers(person, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([AllowAny])
def edit_unit(request, id):
    try:
        unit = UnitModel.objects.get(id=id)
    except UnitModel.DoesNotExist:
        return Response({"error": "واحد یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UnitSerializers(unit, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([AllowAny])
def edit_postwork(request, id):
    try:
        postwork = PostWorkModel.objects.get(id=id)
    except PostWorkModel.DoesNotExist:
        return Response({"error": "واحد یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UnitSerializers(postwork, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([AllowAny])
def edit_worktype(request, id):
    try:
        worktype = WorkTypeModel.objects.get(id=id)
    except WorkTypeModel.DoesNotExist:
        return Response({"error": "واحد یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UnitSerializers(worktype, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        person_code = serializer.validated_data["person_code"]
        password = serializer.validated_data["password"]
        try:
            user = PersonelModel.objects.get(person_code=person_code)
            if user.password == password:
                user_data = PersonGetSerializers(user).data
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "رمز عبور اشتباه است"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except PersonelModel.DoesNotExist:
            return Response(
                {"error": "کاربری با این شماره پرسنلی یافت نشد"},
                status=status.HTTP_404_NOT_FOUND,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "ثبت‌ نام با موفقیت انجام شد"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDataView(APIView):
    def post(self, request):
        person_code = request.data.get("person_code")
        if not person_code:
            return Response(
                {"detail": "کد پرسنلی الزامی است."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            person = PersonelModel.objects.get(person_code=person_code)
        except PersonelModel.DoesNotExist:
            return Response(
                {"detail": "کاربری با این کد پرسنلی وجود ندارد."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PersonGetSerializers(person)
        return Response(serializer.data, status=status.HTTP_200_OK)
