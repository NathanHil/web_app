# Generated by Django 3.2 on 2021-06-29 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0144_auto_20210629_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='bath_count',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=11),
        ),
    ]