# Generated by Django 3.1.3 on 2021-08-18 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0171_auto_20210818_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='note',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
