# Generated by Django 3.2 on 2021-09-27 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0219_accountingtransaction_is_upgrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='tieouttask',
            name='form_order',
            field=models.IntegerField(default=0),
        ),
    ]
