# Generated by Django 3.2 on 2021-11-02 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0204_alter_traffic_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traffic',
            name='date',
            field=models.DateField(),
        ),
    ]
