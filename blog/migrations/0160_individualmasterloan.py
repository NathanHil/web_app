# Generated by Django 3.1.3 on 2021-08-13 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0159_remove_masterloan_masterplans'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualMasterLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterloan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.masterloan')),
                ('masterplantest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.masterplantest')),
            ],
        ),
    ]