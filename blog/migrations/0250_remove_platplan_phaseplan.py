# Generated by Django 3.2 on 2022-01-26 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0249_platplan_phase_plan_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platplan',
            name='phaseplan',
        ),
    ]
