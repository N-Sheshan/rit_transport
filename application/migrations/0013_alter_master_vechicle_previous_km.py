# Generated by Django 5.0.1 on 2024-05-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_rename_previous_us_master_vechicle_previous_km'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_vechicle',
            name='Previous_km',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
