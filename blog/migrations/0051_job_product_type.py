# Generated by Django 3.1.3 on 2021-02-12 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0050_auto_20210210_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='product_type',
            field=models.CharField(choices=[('DFL', 'DFL'), ('DRL', 'DRL'), ('AFL', 'AFL'), ('ARL', 'ARL')], default='DFL', max_length=100),
        ),
    ]
