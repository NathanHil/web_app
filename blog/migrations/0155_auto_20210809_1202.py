# Generated by Django 3.1.3 on 2021-08-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0154_auto_20210809_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='number',
            field=models.BigIntegerField(default=0),
        ),
    ]
