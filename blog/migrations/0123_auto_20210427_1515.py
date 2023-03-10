# Generated by Django 3.1.3 on 2021-04-27 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0122_auto_20210426_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='docs_requested_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='loan_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.job'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='lender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.lender'),
        ),
    ]
