# Generated by Django 5.0.1 on 2024-04-24 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_remove_qr_data_event_name_remove_qr_data_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='QrData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('otp', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='qr_data',
        ),
    ]
