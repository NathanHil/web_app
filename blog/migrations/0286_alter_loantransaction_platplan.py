# Generated by Django 3.2 on 2022-04-06 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0285_alter_loantransaction_purchasingactivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loantransaction',
            name='platplan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.platplan'),
        ),
    ]
