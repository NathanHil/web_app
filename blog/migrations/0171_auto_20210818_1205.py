# Generated by Django 3.1.3 on 2021-08-18 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0170_auto_20210818_1158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='approval_date',
            new_name='appraisal_date',
        ),
        migrations.RenameField(
            model_name='masterloanpackage',
            old_name='approval_date',
            new_name='appraisal_date',
        ),
    ]