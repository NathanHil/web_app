# Generated by Django 3.2 on 2022-04-04 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0281_purchasingactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='loantransaction',
            name='purchasingactivity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='blog.purchasingactivity'),
        ),
    ]