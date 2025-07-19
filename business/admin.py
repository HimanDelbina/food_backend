from django.contrib import admin
from .models import *


# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    fields = ["name", "address", "phone", "ostan", "city"]
    list_display = ["name", "address", "phone", "ostan", "city"]
    search_fields = ["name", "phone"]
    list_filter = ["ostan", "city"]


class ContactPersonAdmin(admin.ModelAdmin):
    fields = ["vendor", "full_name", "phone", "email", "position"]
    list_display = ["full_name", "phone", "email", "position"]
    search_fields = ["full_name", "phone"]
    list_filter = ["position"]


class PurchaseRequestAdmin(admin.ModelAdmin):
    fields = ["requester", "title", "description", "status", "review_comment"]
    list_display = ["requester", "title", "description", "status", "review_comment"]
    search_fields = ["title"]
    list_filter = ["status"]


class PurchaseRequestAttachmentAdmin(admin.ModelAdmin):
    fields = ["request", "file"]
    list_display = ["request", "file"]
    # search_fields = ["title"]
    list_filter = ["request"]


class PurchaseOrderAdmin(admin.ModelAdmin):
    readonly_fields = ["order_date"]
    fields = ["vendor", "status"]
    list_display = ["vendor", "order_date", "status"]
    search_fields = ["vendor__name"]
    list_filter = ["status", "order_date"]


class PurchaseRequestItemAdmin(admin.ModelAdmin):
    fields = ["request", "item", "quantity", "note"]
    list_display = ["request", "item", "quantity", "note"]
    # search_fields = ["title"]
    # list_filter = ["status"]


class GoodsReceiptAdmin(admin.ModelAdmin):
    fields = ["purchase_order", "received_date", "notes"]
    list_display = ["purchase_order", "received_date", "notes"]
    # search_fields = ["title"]
    # list_filter = ["status"]


class InvoiceAdmin(admin.ModelAdmin):
    fields = [
        "purchase_order",
        "invoice_number",
        "amount",
        "issue_date",
        "due_date",
        "is_paid",
    ]
    list_display = [
        "purchase_order",
        "invoice_number",
        "amount",
        "issue_date",
        "due_date",
        "is_paid",
    ]
    search_fields = ["invoice_number"]
    list_filter = ["is_paid"]


class PurchaseOrderItemAdmin(admin.ModelAdmin):
    fields = ["order", "item", "quantity", "unit_price", "request_item"]
    list_display = ["order", "item", "quantity", "unit_price", "request_item"]
    search_fields = ["item"]
    # list_filter = ["is_paid"]


admin.site.register(Vendor, VendorAdmin)
admin.site.register(ContactPerson, ContactPersonAdmin)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
admin.site.register(PurchaseRequestAttachment, PurchaseRequestAttachmentAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseRequestItem, PurchaseRequestItemAdmin)
admin.site.register(GoodsReceipt, GoodsReceiptAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PurchaseOrderItem, PurchaseOrderItemAdmin)
