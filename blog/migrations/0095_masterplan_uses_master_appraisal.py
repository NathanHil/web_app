# Generated by Django 3.1.3 on 2021-03-17 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0094_auto_20210316_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterplan',
            name='uses_master_appraisal',
            field=models.BooleanField(default=1),
        ),
    ]