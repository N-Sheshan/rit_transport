# Generated by Django 5.0.1 on 2024-05-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='master_vechicle',
            name='Previous_us',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
