# Generated by Django 5.0.1 on 2024-05-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_master_vechicle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport_approval',
            name='proof_date',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
