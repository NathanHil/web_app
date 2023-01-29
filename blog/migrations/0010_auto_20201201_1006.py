# Generated by Django 3.1.3 on 2020-12-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201201_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('total_capacity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterModelOptions(
            name='community',
            options={'ordering': ('community_name',)},
        ),
    ]
