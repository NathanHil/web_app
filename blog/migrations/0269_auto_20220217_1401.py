# Generated by Django 3.2 on 2022-02-17 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0268_auto_20220217_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportTaskError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=200)),
                ('importtask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.importtask')),
            ],
        ),
        migrations.DeleteModel(
            name='ImportTaskErrors',
        ),
    ]
