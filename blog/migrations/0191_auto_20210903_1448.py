# Generated by Django 3.1.3 on 2021-09-03 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0190_tieout_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tieout',
            name='review_base_price',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_close_date',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_completion_date',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_levels',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_lot_cost',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_lot_fmv',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_sale_date',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_sqft',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_standard',
        ),
        migrations.RemoveField(
            model_name='tieout',
            name='review_start_date',
        ),
        migrations.CreateModel(
            name='TieOutTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commment', models.CharField(max_length=50)),
                ('name', models.CharField(choices=[('review_standard', 'review_standard'), ('review_sqft', 'review_sql'), ('review_levels', 'review_levels'), ('review_start_date', 'review_start_date')], default=None, max_length=100)),
                ('complete', models.BooleanField(default=0)),
                ('tieout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tieout')),
            ],
        ),
    ]