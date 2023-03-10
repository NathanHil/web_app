# Generated by Django 3.1.3 on 2021-09-13 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0205_salesoption_ss_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountingOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=50, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.job')),
            ],
        ),
        migrations.AddField(
            model_name='salesoption',
            name='accountingoption',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.accountingoption'),
        ),
    ]
