# Generated by Django 3.1.3 on 2021-03-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0092_auto_20210315_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterplan',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved')], max_length=100, null=True),
        ),
    ]