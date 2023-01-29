# Generated by Django 3.1.3 on 2021-03-31 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0107_traffic_plat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traffic',
            name='community',
        ),
        migrations.AlterField(
            model_name='traffic',
            name='plat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.plat'),
        ),
    ]