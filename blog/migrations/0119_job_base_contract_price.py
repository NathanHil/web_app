# Generated by Django 3.1.3 on 2021-04-23 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0118_job_sales_commission'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='base_contract_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]