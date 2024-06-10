# Generated by Django 5.0.1 on 2024-05-23 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_rename_overall_km_transport_approval_ending_km_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master_Vechicle',
            fields=[
                ('vehicle_no', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Usage', models.CharField(blank=True, max_length=100, null=True)),
                ('Driver_Name', models.CharField(blank=True, max_length=100, null=True)),
                ('fule_type', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(blank=True, max_length=100, null=True)),
                ('Driver_Number', models.CharField(blank=True, max_length=100, null=True)),
                ('route_name', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='transport_approval',
            old_name='vechical_no',
            new_name='vehicle_no',
        ),
        migrations.RenameField(
            model_name='transport_approval',
            old_name='vechical_type',
            new_name='vehicle_type',
        ),
    ]