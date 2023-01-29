# Generated by Django 3.2 on 2021-11-12 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0227_auto_20211110_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='procore_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='plat',
            name='procore_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='com_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]