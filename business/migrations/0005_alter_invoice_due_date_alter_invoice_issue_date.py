# Generated by Django 5.2 on 2025-06-23 01:10

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_purchaserequestattachment_uploaded_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ سررسید'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issue_date',
            field=django_jalali.db.models.jDateField(verbose_name='تاریخ صدور'),
        ),
    ]
