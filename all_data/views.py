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

    allowed_types = {"anbar", "leave", "overtime"}

    if types_param:
        types = [t.strip().lower() for t in types_param.split(",")]
        types = [t for t in types if t in allowed_types]
    else:
        types = list(allowed_types)  # اگر چیزی ارسال نشد، همه‌ی نوع‌ها بررسی شوند

    result = {}

    if "anbar" in types:
        anbar_queryset = AnbarRequestModel.objects.filter(status="P")
        if anbar_queryset.exists():
            result["anbar_requests"] = AnbarRequestGetSerializers(
                anbar_queryset, many=True
            ).data

    if "leave" in types:
        # leave_queryset = LeaveRequestModel.objects.filter(...)
        # result["leave_requests"] = LeaveSerializer(leave_queryset, many=True).data
        pass

    if "overtime" in types:
        # overtime_queryset = OvertimeRequestModel.objects.filter(...)
        # result["overtime_requests"] = OvertimeSerializer(overtime_queryset, many=True).data
        pass

    if not result:
        return Response(
            {"error": "هیچ داده‌ای برای درخواست‌های معتبر یافت نشد."}, status=404
        )

    return Response(result, status=200)
