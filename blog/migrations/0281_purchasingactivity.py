# Generated by Django 3.2 on 2022-04-04 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0280_alter_goal_goal_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchasingActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wms_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('costcode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.costcode')),
            ],
        ),
    ]
