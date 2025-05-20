from rest_framework import status
from rest_framework.permissions import AllowAny
from anbar.models import *
from anbar.serializers import *
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from user.models import *


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_requests_by_type(request):
    types_param = request.query_params.get("type")  # مثلا anbar,leave

    if types_param:
        types = [t.strip().lower() for t in types_param.split(",")]
    else:
        types = ["anbar"]  # پیش‌فرض اگر چیزی ارسال نشد
    allowed_types = {"anbar", "leave", "overtime"}
    types = [t for t in types if t in allowed_types]

    result = {}

    if "anbar" in types:
        anbar_queryset = AnbarRequestModel.objects.filter(status="P")
        if anbar_queryset.exists():
            anbar_data = AnbarRequestGetSerializers(anbar_queryset, many=True).data
            result["anbar_requests"] = anbar_data

    # ignore "leave" and "overtime" for now
    unknown_types = [t for t in types if t not in ["anbar"]]
    if unknown_types:
        return Response(
            {"error": f"نوع درخواست‌های نامعتبر: {', '.join(unknown_types)}"}, status=400
        )

    if not result:
        return Response(
            {"error": "هیچ داده‌ای برای درخواست‌های معتبر یافت نشد."}, status=404
        )

    return Response(result, status=200)
