# Generated by Django 3.2 on 2022-03-29 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0278_costcode_is_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='goal_type',
            field=models.CharField(choices=[('annual', 'Annual'), ('reforecast', 'Reforecast')], default='annual', max_length=15, null=True),
        ),
    ]
