# Generated by Django 3.1.3 on 2021-06-09 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0141_alter_plans_plan_long_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plat',
            name='date_posted',
            field=models.DateTimeField(),
        ),
    ]
