# Generated by Django 3.2 on 2022-01-31 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0259_auto_20220131_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='proformamilestone',
            name='proformaplans',
            field=models.ManyToManyField(blank=True, through='blog.ProformaMilestoneDetail', to='blog.ProformaPlan'),
        ),
    ]
