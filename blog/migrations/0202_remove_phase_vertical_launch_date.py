# Generated by Django 3.2 on 2021-09-30 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0201_alter_loantransaction_masterplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phase',
            name='vertical_launch_date',
        ),
    ]
