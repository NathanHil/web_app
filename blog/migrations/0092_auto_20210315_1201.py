# Generated by Django 3.1.3 on 2021-03-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0091_auto_20210312_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='masterplan',
            old_name='loan_committment',
            new_name='approved_commitment',
        ),
        migrations.AddField(
            model_name='masterplan',
            name='approval_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='masterplan',
            name='est_commitment',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='masterplan',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved')], default='Submitted', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='masterplan',
            name='submission_date',
            field=models.DateTimeField(null=True),
        ),
    ]