# Generated by Django 5.2 on 2025-06-23 00:17

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_alter_purchaseorder_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsreceipt',
            name='received_date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ دریافت'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ سررسید'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issue_date',
            field=django_jalali.db.models.jDateTimeField(verbose_name='تاریخ صدور'),
        ),
    ]
