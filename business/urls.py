# urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from . import views

router = DefaultRouter()
router.register(r"vendors", VendorViewSet)
router.register(r"contacts", ContactPersonViewSet)
router.register(r"purchase", PurchaseRequestViewSet)
router.register(r"order", PurchaseOrderViewSet)
router.register(r"goods_receipts", GoodsReceiptViewSet)
router.register(r"invoices", InvoiceViewSet)
router.register(r"purchase_request_attachments", PurchaseRequestAttachmentViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("get_purches", views.get_purches, name="get_purches"),
]
urlpatterns += router.urls
