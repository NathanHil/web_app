# Generated by Django 3.1.3 on 2021-08-17 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0167_auto_20210817_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_commitment', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MasterLoanPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_release', models.IntegerField(default=0)),
                ('receive_cash_back', models.BooleanField(default=0)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('submission_date', models.DateTimeField(blank=True, null=True)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.lender')),
                ('masterplans', models.ManyToManyField(through='blog.MasterLoan', to='blog.MasterPlanTest')),
            ],
        ),
        migrations.AddField(
            model_name='masterloan',
            name='masterloanpackage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.masterloanpackage'),
        ),
        migrations.AddField(
            model_name='masterloan',
            name='masterplantest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.masterplantest'),
        ),
    ]
