# Generated by Django 3.1.3 on 2021-08-17 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0166_phase_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masterloan',
            name='lender',
        ),
        migrations.RemoveField(
            model_name='masterloan',
            name='masterplans',
        ),
        migrations.DeleteModel(
            name='IndividualMasterLoan',
        ),
        migrations.DeleteModel(
            name='MasterLoan',
        ),
    ]
