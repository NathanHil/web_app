# Generated by Django 3.1.3 on 2021-03-23 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0103_auto_20210323_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='width',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=10),
        ),
    ]