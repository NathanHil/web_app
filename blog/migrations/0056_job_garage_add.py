# Generated by Django 3.1.3 on 2021-02-12 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0055_auto_20210212_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='garage_add',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]