# Generated by Django 3.1.3 on 2021-08-20 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0156_auto_20210810_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='past_sheetrock',
            field=models.BooleanField(default=0),
        ),
    ]
