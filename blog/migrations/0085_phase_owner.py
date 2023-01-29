# Generated by Django 3.1.3 on 2021-03-11 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0084_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='phase',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.owner'),
        ),
    ]
