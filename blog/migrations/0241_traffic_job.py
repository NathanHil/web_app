# Generated by Django 3.2 on 2021-12-15 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0240_scheduletask_resource_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='traffic',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.job'),
        ),
    ]
