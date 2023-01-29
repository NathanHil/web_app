# Generated by Django 3.1.3 on 2020-12-01 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201130_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='plat',
            name='build_order',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='sales_tax_rate',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=5),
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=2)),
                ('owner', models.CharField(max_length=100)),
                ('lot_count', models.IntegerField(blank=True, default=0, null=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.community')),
                ('plat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.plat')),
            ],
        ),
    ]
