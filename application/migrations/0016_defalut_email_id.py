# Generated by Django 5.0.6 on 2024-05-29 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_user_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='defalut_email_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.CharField(max_length=100)),
            ],
        ),
    ]
