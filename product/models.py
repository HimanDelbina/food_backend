from django.db import models
from anbar.models import *
from anbar.models import AnbarModel

# Create your models here.


class ProductModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="محصول")
    unit = models.CharField(max_length=20)
    is_active = models.BooleanField(verbose_name="فعال/غیر فعال", default=True)

    class Meta:
        verbose_name = "محصولات تولیدی"
        verbose_name_plural = "محصولات تولیدی"

    def __str__(self):
        return str(self.name)


class ProductMaterialRelation(models.Model):
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, related_name="materials"
    )
    material = models.ForeignKey(
        AnbarModel, on_delete=models.CASCADE, verbose_name="مواد اولیه"
    )
    quantity_per_unit = models.FloatField(
        default=0.0, verbose_name="مقدار مواد اولیه برای تولید هر واحد از محصول"
    )

    class Meta:
        verbose_name = "رابط بین یک محصول نهایی و مواد اولیه"
        verbose_name_plural = "رابط بین یک محصول نهایی و مواد اولیه"

    def __str__(self):
        return str(self.product.name)
