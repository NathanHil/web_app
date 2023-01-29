# Generated by Django 3.1.3 on 2021-05-24 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0134_auto_20210521_0918'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingPermit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('number', models.CharField(blank=True, max_length=30, null=True)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.job')),
            ],
        ),
    ]