from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import AnbarModel
from .serializers import AnbarGetSerializers
from .filters import AnbarModelFilter
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Cast
from user.models import *
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.db import transaction
import jdatetime
from django.utils.timezone import make_aware
from datetime import datetime
from collections import Counter
from django.utils.timezone import now
from datetime import timedelta
from collections import defaultdict
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count

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
def get_complete_request(request):
    user_data = AnbarRequestModel.objects.filter(status = "C")
    return Response(
        AnbarRequestGetSerializers(user_data, many=True).data, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def approve_request_api(request):
    request_id = request.data.get("request_id")
    if not request_id:
        return Response(
            {"error": "request_id الزامی است."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            anbar_request = AnbarRequestModel.objects.get(id=request_id)

            if anbar_request.status not in ["P", "A"]:
                return Response(
                    {
                        "error": f"این درخواست قابل پردازش نیست. وضعیت فعلی: {anbar_request.get_status_display()}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            kala_list = anbar_request.kala

            for item in kala_list:
                code = item.get("code")
                weight_str = item.get("weight")

                if not code or weight_str is None:
                    continue

                try:
                    weight = float(weight_str)
                except (ValueError, TypeError):
                    continue

                try:
                    anbar_item = AnbarModel.objects.select_for_update().get(code=code)
                except AnbarModel.DoesNotExist:
                    return Response(
                        {"error": f"کالایی با کد {code} در انبار یافت نشد."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                try:
                    inventory = float(anbar_item.Inventory)
                except (ValueError, TypeError):
                    inventory = 0.0

                new_inventory = inventory - weight

                if new_inventory < 0:
                    return Response(
                        {"error": f"موجودی کالای {code} کافی نیست."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                anbar_item.Inventory = str(new_inventory)
                anbar_item.save()

            # تنها در صورتی approved_by را ست کنیم که کاربر لاگین کرده باشد
            if (
                hasattr(request.user, "is_authenticated")
                and request.user.is_authenticated
            ):
                anbar_request.approved_by = request.user.personelmodel
            else:
                anbar_request.approved_by = None  # یا هر مقدار پیش‌فرض دیگر

            anbar_request.status = "C"
            anbar_request.approved_at = jdatetime.datetime.now()
            anbar_request.save()

            return Response(
                {"message": "درخواست با موفقیت تکمیل شد و موجودی به‌روز شد."},
                status=status.HTTP_200_OK,
            )

    except AnbarRequestModel.DoesNotExist:
        return Response(
            {"error": "درخواست با این ID یافت نشد."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])  # یا IsAuthenticated بسته به نیازتان
def undo_request_api(request):
    request_id = request.data.get("request_id")

    if not request_id:
        return Response(
            {"error": "request_id الزامی است."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            anbar_request = AnbarRequestModel.objects.select_related("user").get(
                id=request_id
            )

            if anbar_request.status != "C":
                return Response(
                    {
                        "error": f"این درخواست قابل لغو نیست. وضعیت فعلی: {anbar_request.get_status_display()}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            kala_list = anbar_request.kala

            for item in kala_list:
                code = item.get("code")
                quantity = item.get("quantity") or item.get("weight")

                if not code or quantity is None:
                    continue

                try:
                    quantity = float(quantity)
                except (ValueError, TypeError):
                    continue

                try:
                    anbar_item = AnbarModel.objects.select_for_update().get(code=code)
                except AnbarModel.DoesNotExist:
                    return Response(
                        {"error": f"کالایی با کد {code} در انبار یافت نشد."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                try:
                    inventory = float(anbar_item.Inventory)
                except (ValueError, TypeError):
                    inventory = 0.0

                new_inventory = inventory + quantity  # فقط تفاوت با قبل: +

                anbar_item.Inventory = str(new_inventory)
                anbar_item.save()

            # تغییر وضعیت درخواست به "P" یا "R" (Rejected / Reversed)
            anbar_request.status = "U"  # یا 'P' بسته به نیازتان
            anbar_request.save()

            return Response(
                {
                    "message": "درخواست با موفقیت لغو شد و موجودی به انبار بازگردانده شد."
                },
                status=status.HTTP_200_OK,
            )

    except AnbarRequestModel.DoesNotExist:
        return Response(
            {"error": "درخواست با این ID یافت نشد."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["GET"])
# @permission_classes([AllowAny])
# def get_request_userID(request, user_id):
#     data = AnbarRequestModel.objects.filter(user_id=user_id)
#     serializer = AnbarRequestGetSerializers(data, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_request_userID(request, user_id):
    status_param = request.GET.get("status")  # مثلا "P"
    date_param = request.GET.get("date")  # مثلا "1403-02-25"
    filters = {"user_id": user_id}
    if status_param:
        filters["status"] = status_param
    if date_param:
        try:
            j_date = jdatetime.datetime.strptime(date_param, "%Y-%m-%d").date()
            g_date = j_date.togregorian()
            start_of_day = make_aware(
                datetime(g_date.year, g_date.month, g_date.day, 0, 0, 0)
            )
            end_of_day = make_aware(
                datetime(g_date.year, g_date.month, g_date.day, 23, 59, 59)
            )
            filters["create_at__range"] = (start_of_day, end_of_day)
        except ValueError:
            return Response(
                {"error": "فرمت تاریخ اشتباه است. مثال صحیح: 1403-02-25"}, status=400
            )

    data = AnbarRequestModel.objects.filter(**filters)
    serializer = AnbarRequestGetSerializers(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([AllowAny])
@transaction.atomic
def edit_request_anbar(request, id):
    person = get_object_or_404(AnbarRequestModel, id=id)
    serializer = AnbarRequestEditSerializers(person, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["GET"])
@permission_classes([AllowAny])
def get_request_anbar_for_anbar(request):
    requests = AnbarRequestModel.objects.filter(status="A")
    serializer = AnbarRequestGetSerializers(requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class AnbarAnalyticsAPIView(APIView):
    def get(self, request):
        all_items = AnbarModel.objects.all()

        low_inventory = 0
        overstocked_inventory = 0
        low_items = []
        overstocked_items = []

        for item in all_items:
            try:
                current_inventory = int(item.Inventory)
                min_inv = int(item.min_Inventory)
                max_inv = int(item.max_Inventory)
            except (ValueError, TypeError):
                continue

            if current_inventory < min_inv:
                low_inventory += 1
                low_items.append(
                    {
                        "name": item.name,
                        "quantity": current_inventory,
                        "unit_type": item.unit_type,
                    }
                )
            elif current_inventory > max_inv:
                overstocked_inventory += 1
                overstocked_items.append(
                    {
                        "name": item.name,
                        "quantity": current_inventory,
                        "unit_type": item.unit_type,
                    }
                )

        # تعداد درخواست‌ها بر اساس وضعیت
        request_status_qs = AnbarRequestModel.objects.values("status").annotate(
            count=Count("status")
        ).filter(status__in=['P', 'A', 'C', 'R', 'U']) 
        request_status = {item["status"]: item["count"] for item in request_status_qs}

        # کاربران پرتکرار
        top_request_users = (
            AnbarRequestModel.objects.values("user__first_name", "user__last_name")
            .annotate(request_count=Count("id"))
            .order_by("-request_count")[:5]
        )

        # تاییدکنندگان پرتکرار
        top_approvers = (
            AnbarRequestModel.objects.filter(approved_by__isnull=False)
            .values("approved_by__first_name", "approved_by__last_name")
            .annotate(approve_count=Count("id"))
            .order_by("-approve_count")[:5]
        )

        # توزیع برچسب کالاها
        tag_distribution_qs = AnbarModel.objects.values("tag").annotate(
            count=Count("tag")
        )
        tag_distribution = {item["tag"]: item["count"] for item in tag_distribution_qs}

        # توزیع نوع واحد کالا
        unit_type_distribution_qs = AnbarModel.objects.values("unit_type").annotate(
            count=Count("unit_type")
        )
        unit_type_distribution = {
            item["unit_type"]: item["count"] for item in unit_type_distribution_qs
        }

        # توزیع نوع زیرواحد کالا
        sub_unit_type_distribution_qs = AnbarModel.objects.values(
            "sub_unit_type"
        ).annotate(count=Count("sub_unit_type"))
        sub_unit_type_distribution = {
            item["sub_unit_type"]: item["count"]
            for item in sub_unit_type_distribution_qs
        }

        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_requests = AnbarRequestModel.objects.filter(
            create_at__date__gte=thirty_days_ago
        )
        daily_requests = defaultdict(int)

        for req in recent_requests:
            # فرض می‌کنیم create_at یک jdatetime هست
            jalali_date_str = req.create_at.strftime("%Y/%m/%d")  # مثل '1404/02/29'
            daily_requests[jalali_date_str] += 1
        sorted_daily_requests = [
            {"day": day, "count": count}
            for day, count in sorted(
                daily_requests.items(), key=lambda x: x[0], reverse=True
            )
        ]

        all_requested_items = []
        item_request_counter = Counter()  # تعداد درخواست‌هایی که کالا در آن ظاهر شده
        item_quantity_counter = defaultdict(float)  # جمع مقدار (weight یا quantity)
        item_unit_type = {}  # ذخیره unit_type برای هر کالا

        requests = AnbarRequestModel.objects.values_list("kala", flat=True)

        for raw_kala in requests:
            if not raw_kala or not isinstance(raw_kala, list):
                continue

            seen_in_request = set()  # کالاهای دیده شده در این درخواست

            for entry in raw_kala:
                if isinstance(entry, dict):
                    product_name = entry.get("product_name")
                    weight = entry.get("weight", 0)
                    unit_type = entry.get("unit_type", "-")

                    if product_name:
                        # ثبت کالا برای شمارش تعداد درخواست‌ها
                        seen_in_request.add(product_name)

                        # جمع وزن/مقدار کل
                        item_quantity_counter[product_name] += float(weight)

                        # ذخیره نوع واحد (در صورت تغییر، آخرین واحد نگه داشته می‌شود)
                        item_unit_type[product_name] = unit_type

            # افزودن به شمارنده درخواست‌ها
            for name in seen_in_request:
                item_request_counter[name] += 1

        # ساخت لیست خروجی
        top_items = [
            {
                "name": name,
                "unit_type": item_unit_type.get(name, "-"),
                "request_count": item_request_counter[name],
                "total_quantity": item_quantity_counter[name],
            }
            for name in sorted(
                set(item_request_counter.keys()).union(item_quantity_counter.keys()),
                key=lambda x: item_request_counter[x] + item_quantity_counter[x] / 1000,
                reverse=True,
            )[:5]
        ]

        # تحلیل 1: درصد تأیید/رد/در انتظار
        total_requests = AnbarRequestModel.objects.count()

        if total_requests > 0:
            approved_count = AnbarRequestModel.objects.filter(status="C").count()
            rejected_count = AnbarRequestModel.objects.filter(status="R").count()
            pending_count = AnbarRequestModel.objects.filter(status="P").count()
            undone_count = AnbarRequestModel.objects.filter(status="U").count()

            approval_rate = {
                "approved": round((approved_count / total_requests) * 100, 1),
                "rejected": round((rejected_count / total_requests) * 100, 1),
                "pending": round((pending_count / total_requests) * 100, 1),
                "undo": round((undone_count / total_requests) * 100, 1),
            }
        else:
            approval_rate = {"approved": 0, "rejected": 0, "pending": 0, "undone": 0}

        # محاسبه تعداد درخواست‌های رد شده (status = 'R')
        rejected_requests_count = AnbarRequestModel.objects.filter(status="R").count()
        # کاربرانی که بیشترین درخواست رد شده رو دارند
        top_rejected_users = (
            AnbarRequestModel.objects.filter(status="R")
            .values("user__first_name", "user__last_name")
            .annotate(rejected_count=Count("id"))
            .order_by("-rejected_count")[:5]
        )
        # گرفتن تمام درخواست‌های تکمیل شده (status='C')
        completed_requests = AnbarRequestModel.objects.filter(status="C")

        daily_outgoing = defaultdict(float)

        for req in completed_requests:
            jalali_date_str = req.create_at.strftime(
                "%Y/%m/%d"
            )  # بدون نیاز به JalaliDate

            if isinstance(req.kala, list):
                for item in req.kala:
                    if isinstance(item, dict):
                        weight = item.get("weight", 0)
                        daily_outgoing[jalali_date_str] += float(weight)

        # ساخت لیست نهایی با items_in=0 (چون هنوز ورودی نداریم)
        inventory_trend = []
        running_total = 0  # موجودی فعلی (منفی تا ورودی نداشته باشیم)

        for day in sorted(daily_outgoing.keys()):
            outgoing = daily_outgoing[day]
            running_total -= outgoing
            inventory_trend.append(
                {
                    "date": day,
                    "items_in": 0,
                    "items_out": outgoing,
                    "total_inventory": round(running_total, 2),
                }
            )

        data = {
            "inventory": {
                "low": low_inventory,
                "low_items": low_items,
                "overstocked": overstocked_inventory,
                "overstocked_items": overstocked_items,
            },
            "request_status": request_status,
            "top_request_users": list(top_request_users),
            "top_approvers": list(top_approvers),
            "requests_last_30_days": sorted_daily_requests,
            "tag_distribution": tag_distribution,
            "unit_type_distribution": unit_type_distribution,
            "sub_unit_type_distribution": sub_unit_type_distribution,
            "top_requested_items": top_items,
            "approval_rate": approval_rate,
            "rejected_reasons": rejected_requests_count,
            "top_rejected_users": list(top_rejected_users),
            "inventory_trend": inventory_trend,
        }

        return Response(data)
