# Generated by Django 3.1.3 on 2021-01-13 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_auto_20210112_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proformalist',
            name='sales_base_price',
        ),
        migrations.AlterField(
            model_name='proformalist',
            name='update_description',
            field=models.CharField(choices=[('DM', 'Diligence Mtg'), ('PRM', 'Phase Release Mtg'), ('BARM', 'Bi-Annual Review Mtg')], default='DM', max_length=100),
        ),
        migrations.DeleteModel(
            name='Proforma',
        ),
    ]
