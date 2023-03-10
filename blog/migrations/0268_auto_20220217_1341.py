# Generated by Django 3.2 on 2022-02-17 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0267_auto_20220209_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('failed', models.BooleanField(default=0)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='communityplan',
            options={'ordering': ('name',)},
        ),
        migrations.CreateModel(
            name='ImportTaskErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.importtask')),
            ],
        ),
    ]
