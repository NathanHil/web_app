# Generated by Django 3.1.3 on 2020-12-01 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201130_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phase',
            name='community',
        ),
    ]
