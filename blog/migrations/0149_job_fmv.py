# Generated by Django 3.1.3 on 2021-07-08 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0148_auto_20210706_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='fmv',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
