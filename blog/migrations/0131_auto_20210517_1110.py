# Generated by Django 3.2 on 2021-05-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0130_auto_20210504_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traffic',
            name='be_back_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='traffic',
            name='traffic_count',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ProformaList',
        ),
    ]
