# Generated by Django 3.1.3 on 2021-01-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_auto_20210104_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='construction_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_use',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
