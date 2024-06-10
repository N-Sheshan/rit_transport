# Generated by Django 5.0.1 on 2024-05-23 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_transport_approval_buying_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transport_approval',
            old_name='overall_km',
            new_name='Ending_KM',
        ),
        migrations.RenameField(
            model_name='transport_approval',
            old_name='fuel_amount',
            new_name='fuel_quantity',
        ),
        migrations.AddField(
            model_name='transport_approval',
            name='Mileage',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transport_approval',
            name='starting_KM',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
