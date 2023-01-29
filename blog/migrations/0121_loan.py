# Generated by Django 3.1.3 on 2021-04-26 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0120_job_list_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closing_date', models.DateField()),
                ('maturity_date', models.DateField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.job')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.costcode')),
            ],
        ),
    ]