# Generated by Django 3.2 on 2022-01-26 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0247_plat_plans'),
    ]

    operations = [
        migrations.AddField(
            model_name='loantransaction',
            name='platplan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.platplan'),
        ),
        migrations.AddField(
            model_name='platplan',
            name='phaseplan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.phaseplan'),
        ),
    ]