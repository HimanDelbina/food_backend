# Generated by Django 5.2 on 2025-07-19 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_destinationmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personelmodel',
            name='child',
            field=models.ManyToManyField(blank=True, to='user.childmodel', verbose_name='فرزند'),
        ),
    ]
