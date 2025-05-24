from random import choices
from django.db import models
import os
from django.conf import settings
from product.models import *
from user.models import *
from django_jalali.db import models as jmodels

EXPORTORDOMESTIC = (
    ("S", "صادراتی"),
    ("D", "داخلی"),
)


class TolidModel(models.Model):
    user = models.ForeignKey(
        PersonelModel, verbose_name="تولید کننده", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        ProductModel, verbose_name="کالای تولیدی", on_delete=models.CASCADE
    )
    production = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="موجودی تولیدی", default=0
    )
    batch_number = models.CharField(
        max_length=100, verbose_name="کد کالا", null=True, blank=True
    )
    is_export = models.CharField(
        verbose_name="صادراتی یا داخلی", choices=EXPORTORDOMESTIC, max_length=1
    )
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    expiration_date = jmodels.jDateField(
        verbose_name="تاریخ انقضا ",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    production_date = jmodels.jDateField(
        verbose_name="تاریخ تولید ",
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
    )
    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصول"

    def __str__(self):
        return self.product.name


class AnbarGhModel(models.Model):
    tolid_item = models.ForeignKey(
        TolidModel, verbose_name="محصول", on_delete=models.CASCADE
    )
    total_inventory = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="موجودی کل", default=0
    )
    start_date = jmodels.jDateField(
        verbose_name="تاریخ ورود به انبار قرنطینه",
        auto_now_add=True,
        null=True,
        blank=True,
    )
    end_date = jmodels.jDateField(
        verbose_name="تاریخ خروج به انبار قرنطینه",
        auto_now_add=False,
        null=True,
        blank=True,
    )

    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "انبار قرنطینه محصول"
        verbose_name_plural = "انبار قرنطینه محصول"

    def __str__(self):
        return f"{self.tolid_item} | باقیمانده: {self.remaining_inventory} {self.unit}"


class AnbarTolidModel(models.Model):
    tolid_item = models.ForeignKey(
        TolidModel, verbose_name="محصول", on_delete=models.CASCADE
    )
    total_inventory = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="موجودی کل", default=0
    )
    remaining_inventory = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="موجودی باقی‌مانده", default=0
    )

    create_at = jmodels.jDateTimeField(auto_now_add=True)
    update_at = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "انبار محصول"
        verbose_name_plural = "انبار محصول"

    def __str__(self):
        return f"{self.tolid_item} | باقیمانده: {self.remaining_inventory} {self.unit}"


class AnbarExitModel(models.Model):
    anbar_item = models.ForeignKey(
        AnbarTolidModel, on_delete=models.CASCADE, verbose_name="کالای انبار"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="مقدار خروجی"
    )
    destination = models.ForeignKey(
        DestinationModel, verbose_name="مشتری", on_delete=models.CASCADE
    )
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    exit_date = jmodels.jDateField(verbose_name="تاریخ خروج", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.amount > self.anbar_item.remaining_inventory:
                raise ValueError("مقدار خروجی بیشتر از موجودی باقی‌مانده است.")
            self.anbar_item.remaining_inventory -= self.amount
            self.anbar_item.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "خروجی انبار محصول"
        verbose_name_plural = "خروجی انبار محصول"

    def __str__(self):
        return f"{self.amount} {self.anbar_item.unit} از {self.anbar_item}"
