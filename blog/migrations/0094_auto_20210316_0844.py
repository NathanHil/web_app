# Generated by Django 3.1.3 on 2021-03-16 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0093_auto_20210315_1205'),
    ]

    operations = [

        migrations.AlterField(
            model_name='masterplan',
            name='approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='masterplan',
            name='status',
            field=models.CharField(blank=True, choices=[('Submitted', 'Submitted'), ('Approved', 'Approved')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='masterplan',
            name='submission_date',
            field=models.DateTimeField(blank=True, null=True),
        ),

    ]
