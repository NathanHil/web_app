# Generated by Django 3.1.3 on 2021-03-30 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0105_merge_20210330_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traffic',
            name='name',
        ),
    ]
