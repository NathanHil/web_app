# Generated by Django 3.1.3 on 2021-02-18 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_plans_is_attached'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='plan',
            field=models.CharField(max_length=50),
        ),
    ]