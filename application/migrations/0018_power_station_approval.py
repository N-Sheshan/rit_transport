# Generated by Django 5.0.6 on 2024-06-10 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_alter_transport_approval_fuel_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='power_station_approval',
            fields=[
                ('bill_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('generater_no', models.CharField(blank=True, max_length=100, null=True)),
                ('fule_type', models.CharField(blank=True, max_length=100, null=True)),
                ('buying_date', models.DateField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=500, null=True)),
                ('fuel_quantity', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('billed_date', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]