# Generated by Django 3.1.3 on 2021-08-20 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0176_auto_20210820_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='loantransaction',
            name='masterloan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.masterloan'),
        ),
    ]
