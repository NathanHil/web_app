# Generated by Django 3.1.3 on 2020-12-08 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_remove_proformalist_tied_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='proformalist',
            name='update_code',
            field=models.CharField(choices=[('DM', 'Diligence Mtg'), ('PRM', 'Phase Release Mtg'), ('BARM', 'Bi-Annual Review Mtg')], default='DM', max_length=100),
        ),
        migrations.AlterField(
            model_name='proformalist',
            name='update_date',
            field=models.DateField(null=True),
        ),
    ]
