# Generated by Django 5.2 on 2025-06-23 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anbar', '0008_anbarrequestmodel_request_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anbarmodel',
            name='Inventory',
            field=models.FloatField(default=0.0, verbose_name='موجودی'),
        ),
    ]
