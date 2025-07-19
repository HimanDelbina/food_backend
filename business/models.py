from django.db import models
from user.models import *
from anbar.models import *
from django_jalali.db import models as jmodels


class Vendor(models.Model):
    name = models.CharField("نام شرکت", max_length=255)
    address = models.TextField("آدرس", blank=True, null=True)
    phone = models.CharField("شماره تماس", max_length=20, blank=True, null=True)
    ostan = models.ForeignKey(
        OstanModel,
        verbose_name="استان",
        on_delete=models.CASCADE,
        related_name="ostan",
    )
    city = models.ForeignKey(
        CityModel,
        verbose_name="شهرستان",
        on_delete=models.CASCADE,
        related_name="city",
    )

    class Meta:
        verbose_name = "تأمین‌کننده"
        verbose_name_plural = "تأمین‌کنندگان"

    def __str__(self):
        return self.name


class ContactPerson(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="contacts"
    )
    full_name = models.CharField("نام کامل", max_length=255)
    phone = models.CharField("شماره تماس", max_length=20, blank=True, null=True)
    email = models.EmailField("ایمیل", blank=True, null=True)
    position = models.CharField("سمت", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "شخص تماس"
        verbose_name_plural = "افراد تماس"

    def __str__(self):
        return f"{self.full_name} ({self.vendor.name})"


class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار بررسی"),
        ("approved", "تأیید شده"),
        ("rejected", "رد شده"),
    ]

    requester = models.ForeignKey(
        PersonelModel, on_delete=models.CASCADE, verbose_name="درخواست‌دهنده"
    )
    title = models.CharField("عنوان درخواست", max_length=255)
    description = models.TextField("توضیحات", blank=True, null=True)
    status = models.CharField(
        "وضعیت", max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    review_comment = models.TextField("یادداشت مدیر", blank=True, null=True)
    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "درخواست خرید"
        verbose_name_plural = "درخواست‌های خرید"

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class PurchaseRequestAttachment(models.Model):
    request = models.ForeignKey(
        PurchaseRequest, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to="purchase_requests/")
    uploaded_at = jmodels.jDateTimeField(auto_now_add=True)


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, verbose_name="تأمین‌کننده"
    )
    order_date = jmodels.jDateTimeField("تاریخ سفارش", auto_now_add=True)
    status = models.CharField(
        "وضعیت سفارش",
        max_length=50,
        choices=[
            ("draft", "پیش‌نویس"),
            ("editing", "ویرایش بشه"),
            ("approved", "تأیید شده"),
            ("shipped", "ارسال شده"),
            ("received", "دریافت شده"),
            ("cancelled", "لغو شده"),
        ],
        default="draft",
    )
    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سفارش خرید"
        verbose_name_plural = "سفارش‌های خرید"

    def __str__(self):
        return f"PO#{self.id} - {self.vendor.name}"


class PurchaseRequestItem(models.Model):
    request = models.ForeignKey(
        PurchaseRequest,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="درخواست",
    )
    item = models.ForeignKey(
        AnbarModel,
        on_delete=models.CASCADE,
        verbose_name="کالای درخواستی",
    )
    quantity = models.PositiveIntegerField("تعداد")
    note = models.TextField("توضیحات", blank=True, null=True)

    class Meta:
        verbose_name = "آیتم درخواست خرید"
        verbose_name_plural = "آیتم‌های درخواست خرید"

    def __str__(self):
        return f"{self.item.name} × {self.quantity}"


class GoodsReceipt(models.Model):
    purchase_order = models.OneToOneField(
        PurchaseOrder, on_delete=models.CASCADE, verbose_name="سفارش خرید"
    )
    received_date = jmodels.jDateTimeField("تاریخ دریافت", auto_now_add=True)
    notes = models.TextField("یادداشت‌ها", blank=True, null=True)

    class Meta:
        verbose_name = "رسید کالا"
        verbose_name_plural = "رسیدهای کالا"


class Invoice(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, verbose_name="سفارش خرید"
    )
    invoice_number = models.CharField("شماره فاکتور", max_length=100)
    amount = models.DecimalField("مبلغ", max_digits=12, decimal_places=2)
    issue_date = jmodels.jDateField("تاریخ صدور")
    due_date = jmodels.jDateField("تاریخ سررسید", blank=True, null=True)
    is_paid = models.BooleanField("پرداخت شده", default=False)

    class Meta:
        verbose_name = "فاکتور خرید"
        verbose_name_plural = "فاکتورهای خرید"

    def __str__(self):
        return self.invoice_number


class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش",
    )
    item = models.ForeignKey(
        AnbarModel,
        on_delete=models.CASCADE,
        verbose_name="کالای سفارش‌داده‌شده",
    )
    quantity = models.PositiveIntegerField("تعداد")
    unit_price = models.FloatField("قیمت واحد")
    request_item = models.ForeignKey(
        PurchaseRequestItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="آیتم درخواست مرتبط",
    )
    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "آیتم سفارش خرید"
        verbose_name_plural = "آیتم‌های سفارش خرید"

    def total_price(self):
        return self.unit_price * self.quantity
