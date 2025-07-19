from django.db import models
from user.models import *
from django_jalali.db import models as jmodels


class PasswordItem(models.Model):
    user = models.ForeignKey(
        PersonelModel, on_delete=models.CASCADE, related_name="passwords"
    )
    title = models.CharField(max_length=100, verbose_name="عنوان رمز")
    username = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="نام کاربری"
    )
    password = models.CharField(max_length=255, verbose_name="رمز عبور")
    note = models.TextField(blank=True, null=True, verbose_name="یادداشت")
    create_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "رمزهای عبور"
        verbose_name_plural = "رمزهای عبور"

    def __str__(self):
        return f"{self.title} for {self.user.first_name}"
