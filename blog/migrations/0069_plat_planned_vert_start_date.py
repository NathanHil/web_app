# Generated by Django 3.1.3 on 2021-03-02 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0068_lender'),
    ]

    operations = [
        migrations.AddField(
            model_name='plat',
            name='planned_vert_start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
