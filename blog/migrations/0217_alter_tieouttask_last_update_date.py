# Generated by Django 3.2 on 2021-09-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0216_auto_20210923_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tieouttask',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]