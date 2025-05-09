from django.db import models
import os
from django.conf import settings
from barcode import Code128
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from user.models import *
from django_jalali.db import models as jmodels

UNIT_TYPE = (
    ("A", "عدد"),
    ("KG", "كيلوگرم"),
    ("GE", "گرم"),
    ("LI", "لیتر"),
    ("GA", "گالن"),
)
SUB_UNIT_TYPE = (
    ("KI", "كيسه"),
    ("KA", "كارتن"),
    ("KG", "كيلوگرم"),
    ("GA", "گالن"),
    ("BA", "بسته"),
)
KALA_TAG = (
    ("A", "انبار اجناس"),
    ("K", "انبار مواد"),
)


class AnbarModel(models.Model):
    code = models.CharField(verbose_name="کد کالا", max_length=50)
    name = models.CharField(verbose_name="نام انبار", max_length=50)
    barcode = models.ImageField(
        verbose_name="بارکد",
        upload_to="barcodes/",  # مسیر ذخیره بارکدها
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )
    barcode_address = models.CharField(
        verbose_name="مسیر بارکد", max_length=250, null=True, blank=True
    )
    iran_code = models.CharField(
        verbose_name="ايران كد كالا", max_length=50, null=True, blank=True
    )
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    Inventory = models.CharField(verbose_name="موجودی", max_length=50, default=0)
    min_Inventory = models.CharField(
        verbose_name="حداقل موجودي", max_length=50, default=0
    )
    max_Inventory = models.CharField(
        verbose_name="حداكثر موجودي", max_length=50, default=0
    )
    unit_type = models.CharField(
        verbose_name="واحد اصلي", max_length=2, choices=UNIT_TYPE
    )
    sub_unit_type = models.CharField(
        verbose_name="واحد فرعی", max_length=2, choices=SUB_UNIT_TYPE
    )
    tag = models.CharField(verbose_name="تگ", max_length=2, choices=KALA_TAG)

    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبار"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # اگر بارکد وجود نداشت، بارکد بساز
        if not self.barcode:
            barcode_value = self.code or self.name
            barcode_obj = Code128(barcode_value, writer=ImageWriter())
            buffer = ContentFile(b"")
            barcode_obj.write(buffer)
            filename = f"{barcode_value}.png"
            self.barcode.save(filename, buffer, save=False)
            self.barcode_address = os.path.join("barcodes", filename)
        super().save(*args, **kwargs)


REQUEST_STATUS_CHOICES = (
    ("P", "در انتظار بررسی"),  # Pending
    ("A", "تایید شده"),  # Approved
    ("R", "رد شده"),  # Rejected
    ("C", "تکمیل شده"),  # Completed
)


class AnbarRequestModel(models.Model):
    user = models.ForeignKey(
        PersonelModel, verbose_name="کاربر", on_delete=models.CASCADE
    )
    kala = models.JSONField(verbose_name="کالا ها", default=list)
    description = models.TextField(
        verbose_name="توضیحات/دلیل درخواست", null=True, blank=True
    )  # Added description
    status = models.CharField(
        max_length=1,
        choices=REQUEST_STATUS_CHOICES,
        default="P",  # Default to Pending
        verbose_name="وضعیت درخواست",
    )  # Added status
    approved_by = models.ForeignKey(
        PersonelModel,
        verbose_name="تایید کننده",
        on_delete=models.SET_NULL,  # Keep request even if approver is deleted
        related_name="approved_requests",
        null=True,
        blank=True,
    )
    approved_at = jmodels.jDateTimeField(
        verbose_name="تاریخ تایید/رد", null=True, blank=True
    )
    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "درخواست کالا"
        verbose_name_plural = "درخواست کالا"
        ordering = ["-create_at"]  # Optional: Order requests by creation date

    def __str__(self):
        # Display user and status for better representation
        return f"{self.user.first_name} {self.user.last_name} - {self.get_status_display()}"

    def get_kala_details(self):
        from .models import AnbarModel

        result = []
        for item in self.kala:
            if "kala_id" not in item:
                continue
            try:
                # جستجو بر اساس id
                kala_obj = AnbarModel.objects.get(id=item["kala_id"])  # تغییر این خط
                result.append(
                    {
                        "name": kala_obj.name,
                        "code": kala_obj.code,
                        "id": kala_obj.id,
                        "count": item.get(
                            "quantity", 0
                        ),  # quantity از kala گرفته می‌شود
                    }
                )
            except AnbarModel.DoesNotExist:
                continue
        return result
