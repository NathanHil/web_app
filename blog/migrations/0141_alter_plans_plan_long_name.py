# Generated by Django 3.2 on 2021-06-08 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0140_auto_20210607_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='plan_long_name',
            field=models.CharField(default='none', max_length=50, verbose_name='Plan name'),
        ),
    ]
