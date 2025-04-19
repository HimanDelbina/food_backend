from django.db import models
import os
from django.conf import settings
from barcode import Code128
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile

# Create your models here.


class ShopGroupModel(models.Model):
    name = models.CharField(verbose_name="گروه خريد", max_length=50)

    class Meta:
        verbose_name = "گروه خريد"
        verbose_name_plural = "گروه خريد"

    def __str__(self):
        return self.name


class SellGroupModel(models.Model):
    name = models.CharField(verbose_name="گروه فروش", max_length=50)

    class Meta:
        verbose_name = "گروه فروش"
        verbose_name_plural = "گروه فروش"

    def __str__(self):
        return self.name


class KalaGroupModel(models.Model):
    name = models.CharField(verbose_name="گروه کالا", max_length=50)

    class Meta:
        verbose_name = "گروه کالا"
        verbose_name_plural = "گروه کالا"

    def __str__(self):
        return self.name


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
    shop_group = models.ForeignKey(
        ShopGroupModel,
        verbose_name="گروه خريد",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sell_groupe = models.ForeignKey(
        SellGroupModel,
        verbose_name="گروه فروش",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    kala_group = models.ForeignKey(
        KalaGroupModel,
        verbose_name="گروه کالا",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
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
