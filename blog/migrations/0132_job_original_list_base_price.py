# Generated by Django 3.1.3 on 2021-05-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0131_auto_20210517_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='original_list_base_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
