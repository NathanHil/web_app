# Generated by Django 3.1.3 on 2021-09-08 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0191_auto_20210908_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterloan',
            name='masterloanpackage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.masterloanpackage'),
        ),
    ]
