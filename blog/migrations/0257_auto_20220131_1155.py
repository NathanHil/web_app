# Generated by Django 3.2 on 2022-01-31 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0256_auto_20220128_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proformadetail',
            name='platplan',
        ),
        migrations.RemoveField(
            model_name='proformadetail',
            name='proforma',
        ),
        migrations.DeleteModel(
            name='Proforma',
        ),
        migrations.DeleteModel(
            name='ProformaDetail',
        ),
    ]
