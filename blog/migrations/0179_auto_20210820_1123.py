# Generated by Django 3.1.3 on 2021-08-20 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0178_auto_20210820_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loantransaction',
            name='phaseplan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.phaseplan'),
        ),
    ]
