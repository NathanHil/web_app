# Generated by Django 3.1.3 on 2021-01-13 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_auto_20210112_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_price', models.IntegerField(default=0)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.community')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.plans')),
            ],
            options={
                'unique_together': {('community', 'plan')},
            },
        ),
        migrations.CreateModel(
            name='PricingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_price', models.IntegerField(default=0)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.pricing')),
            ],
        ),
    ]