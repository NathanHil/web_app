# Generated by Django 3.1.3 on 2020-12-11 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20201210_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase',
            name='plat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.plat'),
        ),
        migrations.CreateModel(
            name='PlatSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_name', models.CharField(max_length=30)),
                ('milestone', models.CharField(max_length=30)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('finish', models.DateField(blank=True, null=True)),
                ('task', models.CharField(max_length=30)),
                ('cash_needs', models.IntegerField(default=0)),
                ('smartsheet_row_id', models.CharField(max_length=100)),
                ('plat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.plat')),
            ],
        ),
        migrations.CreateModel(
            name='GenSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_name', models.CharField(max_length=30)),
                ('milestone', models.CharField(max_length=30)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('finish', models.DateField(blank=True, null=True)),
                ('task', models.CharField(max_length=30)),
                ('cash_needs', models.IntegerField(default=0)),
                ('smartsheet_row_id', models.CharField(max_length=100)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.community')),
            ],
        ),
    ]
