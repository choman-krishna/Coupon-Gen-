# Generated by Django 5.0.1 on 2024-04-27 08:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_delete_qrdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScannedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('scanned_otp', models.CharField(max_length=20)),
                ('scanned_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp_status', models.CharField(max_length=20)),
            ],
        ),
    ]
