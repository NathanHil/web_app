# Generated by Django 3.1.3 on 2021-02-15 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0059_auto_20210215_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='plans',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
    ]
