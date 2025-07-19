from rest_framework import serializers
from .models import *
from anbar.models import *
from user.models import *
from user.serializers import *


class AnbarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnbarModel
        fields = "__all__"


class ContactPersonSerializer(serializers.ModelSerializer):
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(), source="vendor"
    )
    vendor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ContactPerson
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    contacts = ContactPersonSerializer(many=True, read_only=True)
    ostan = OstanSerializers(read_only=True)
    city = CitySerializers(read_only=True)
    ostan_id = serializers.PrimaryKeyRelatedField(
        queryset=OstanModel.objects.all(), source="ostan", write_only=True
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=CityModel.objects.all(), source="city", write_only=True
    )

    class Meta:
        model = Vendor
        fields = "__all__"


class PurchaseRequestItemSerializer(serializers.ModelSerializer):
    item = AnbarModelSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=AnbarModel.objects.all(), source="item", write_only=True
    )

    class Meta:
        model = PurchaseRequestItem
        fields = ["id", "item", "item_id", "quantity", "note"]


class PurchaseRequestAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestAttachment
        fields = ["id", "file", "uploaded_at"]


class PurchaseRequestItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = PurchaseRequestItem
        fields = ["id", "item", "item_name", "quantity", "note"]


# class PurchaseRequestSerializer(serializers.ModelSerializer):
#     items = PurchaseRequestItemSerializer(many=True)

#     class Meta:
#         model = PurchaseRequest
#         fields = [
#             "id",
#             "requester",
#             "title",
#             "description",
#             "status",
#             "review_comment",
#             "create_at",
#             "update_at",
#             "items",
#         ]
#         read_only_fields = ["status", "review_comment", "create_at", "update_at"]

#     def update(self, instance, validated_data):
#         items_data = validated_data.pop("items", None)

#         # آپدیت فیلدهای ساده
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()

#         if items_data is not None:
#             # نگاشت id های موجود
#             existing_item_ids = [item.id for item in instance.items.all()]
#             sent_item_ids = [item.get("id") for item in items_data if item.get("id")]

#             # حذف آیتم هایی که در درخواست جدید نیستن
#             for item_id in existing_item_ids:
#                 if item_id not in sent_item_ids:
#                     PurchaseRequestItem.objects.filter(id=item_id).delete()

#             # اضافه یا آپدیت آیتم‌ها
#             for item_data in items_data:
#                 item_id = item_data.get("id", None)
#                 if item_id:
#                     # آپدیت آیتم موجود
#                     item_instance = PurchaseRequestItem.objects.get(
#                         id=item_id, request=instance
#                     )
#                     for attr, value in item_data.items():
#                         setattr(item_instance, attr, value)
#                     item_instance.save()
#                 else:
#                     # ایجاد آیتم جدید
#                     PurchaseRequestItem.objects.create(request=instance, **item_data)


#         return instance


class RequesterSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelModel  # یا هر مدلی که به requester وصل هست
        fields = ["first_name", "last_name"]


class PurchaseRequestGetSerializer(serializers.ModelSerializer):
    requester = RequesterSummarySerializer()

    class Meta:
        model = PurchaseRequest
        fields = "__all__"


class PurchaseRequestSerializer(serializers.ModelSerializer):
    items = PurchaseRequestItemSerializer(many=True)
    requester_name = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseRequest
        fields = [
            "id",
            "requester",
            "requester_name",
            "title",
            "description",
            "status",
            "review_comment",
            "create_at",
            "update_at",
            "items",
        ]
        read_only_fields = ["status", "review_comment", "create_at", "update_at"]

    def get_requester_name(self, obj):
        if obj.requester:
            return f"{obj.requester.first_name} {obj.requester.last_name}"
        return None

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])

        purchase_request = PurchaseRequest.objects.create(**validated_data)

        for item_data in items_data:
            PurchaseRequestItem.objects.create(request=purchase_request, **item_data)

        return purchase_request

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            existing_item_ids = [item.id for item in instance.items.all()]
            sent_item_ids = [item.get("id") for item in items_data if item.get("id")]

            for item_id in existing_item_ids:
                if item_id not in sent_item_ids:
                    PurchaseRequestItem.objects.filter(id=item_id).delete()

            for item_data in items_data:
                item_id = item_data.get("id", None)
                if item_id:
                    item_instance = PurchaseRequestItem.objects.get(
                        id=item_id, request=instance
                    )
                    for attr, value in item_data.items():
                        setattr(item_instance, attr, value)
                    item_instance.save()
                else:
                    PurchaseRequestItem.objects.create(request=instance, **item_data)

        return instance


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    request_item_id = serializers.IntegerField(source="request_item.id", read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = [
            "id",
            "item",
            "item_name",
            "quantity",
            "unit_price",
            "request_item",
            "request_item_id",
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "vendor",
            "vendor_name",
            "order_date",
            "status",
            "create_at",
            "update_at",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        for item_data in items_data:
            PurchaseOrderItem.objects.create(order=purchase_order, **item_data)
        return purchase_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                PurchaseOrderItem.objects.create(order=instance, **item_data)

        return instance


class PurchaseOrderMiniSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ["id", "vendor_name", "order_date", "status"]


class GoodsReceiptSerializer(serializers.ModelSerializer):
    purchase_order = PurchaseOrderMiniSerializer(read_only=True)

    class Meta:
        model = GoodsReceipt
        fields = "__all__"
        read_only_fields = ["received_date"]

    def create(self, validated_data):
        order = validated_data["purchase_order"]

        if order.status != "shipped":
            raise serializers.ValidationError("وضعیت سفارش باید 'ارسال شده' باشد.")

        # افزایش موجودی کالاها
        for item in order.items.all():
            item.item.Inventory = str(int(item.item.Inventory) + item.quantity)
            item.item.save()

        # تغییر وضعیت سفارش به 'received'
        order.status = "received"
        order.save()

        return super().create(validated_data)


class InvoiceSerializer(serializers.ModelSerializer):
    purchase_order_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "purchase_order",
            "purchase_order_info",
            "invoice_number",
            "amount",
            "issue_date",
            "due_date",
            "is_paid",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.issue_date:
            data["issue_date"] = instance.issue_date.strftime("%Y-%m-%d")
        if instance.due_date:
            data["due_date"] = instance.due_date.strftime("%Y-%m-%d")
        return data

    def get_purchase_order_info(self, obj):
        return {
            "id": obj.purchase_order.id,
            "vendor": obj.purchase_order.vendor.name,
            "order_date": (
                obj.purchase_order.order_date.strftime("%Y-%m-%d")
                if obj.purchase_order.order_date
                else None
            ),
            "status": obj.purchase_order.status,
        }


class PurchaseRequestAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestAttachment
        fields = ["id", "request", "file", "uploaded_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.uploaded_at:
            data["uploaded_at"] = instance.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
        return data
