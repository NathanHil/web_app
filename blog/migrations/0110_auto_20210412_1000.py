# Generated by Django 3.1.3 on 2021-04-12 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0109_lender_credit_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plat',
            name='status',
            field=models.CharField(choices=[('LD Diligence', 'LD Diligence'), ('LD Future', 'LD Future'), ('LD Construction', 'LD Construction'), ('LD Complete', 'LD Complete'), ('Recorded', 'Recorded'), ('Vertical', 'Vertical')], default='LD Future', max_length=30),
        ),
    ]
