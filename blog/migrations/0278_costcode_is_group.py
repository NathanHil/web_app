# Generated by Django 3.2 on 2022-03-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0277_auto_20220324_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='costcode',
            name='is_group',
            field=models.BooleanField(default=0),
        ),
    ]