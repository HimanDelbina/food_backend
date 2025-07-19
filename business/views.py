from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]


class ContactPersonViewSet(viewsets.ModelViewSet):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get("vendor_id")
        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset


class PurchaseRequestViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequest.objects.all()
    serializer_class = PurchaseRequestSerializer
    permission_classes = [permissions.AllowAny]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["vendor"]


class GoodsReceiptViewSet(viewsets.ModelViewSet):
    queryset = GoodsReceipt.objects.all()
    serializer_class = GoodsReceiptSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["purchase_order"]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["purchase_order__vendor"]


class PurchaseRequestAttachmentViewSet(viewsets.ModelViewSet):
    queryset = PurchaseRequestAttachment.objects.all()
    serializer_class = PurchaseRequestAttachmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["request"]


@api_view(["GET"])
@permission_classes([AllowAny])
def get_purches(request):
    user_data = PurchaseRequest.objects.all()
    return Response(
        PurchaseRequestGetSerializer(user_data, many=True).data,
        status=status.HTTP_200_OK,
    )
