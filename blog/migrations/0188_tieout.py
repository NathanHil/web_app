# Generated by Django 3.1.3 on 2021-09-02 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0187_merge_20210901_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='TieOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_standard', models.BooleanField(default=0)),
                ('review_sqft', models.BooleanField(default=0)),
                ('review_levels', models.BooleanField(default=0)),
                ('review_start_date', models.BooleanField(default=0)),
                ('review_completion_date', models.BooleanField(default=0)),
                ('review_sale_date', models.BooleanField(default=0)),
                ('review_close_date', models.BooleanField(default=0)),
                ('review_base_price', models.BooleanField(default=0)),
                ('review_lot_cost', models.BooleanField(default=0)),
                ('review_lot_fmv', models.BooleanField(default=0)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.job')),
            ],
        ),
    ]