# Generated by Django 3.1.3 on 2021-09-03 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0192_auto_20210903_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tieouttask',
            old_name='commment',
            new_name='comment',
        ),
        migrations.AlterField(
            model_name='tieouttask',
            name='name',
            field=models.CharField(choices=[('review_standard', 'review_standard'), ('review_sqft', 'review_sqft'), ('review_levels', 'review_levels'), ('review_start_date', 'review_start_date')], default=None, max_length=100),
        ),
    ]
