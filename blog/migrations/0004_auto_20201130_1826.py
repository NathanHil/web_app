# Generated by Django 3.1.3 on 2020-12-01 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201130_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='excise_tax_rate',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='community',
            name='sales_tax_rate',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=5),
        ),
    ]
