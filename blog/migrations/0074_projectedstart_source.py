# Generated by Django 3.1.3 on 2021-03-08 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0073_plans_load'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectedstart',
            name='source',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
