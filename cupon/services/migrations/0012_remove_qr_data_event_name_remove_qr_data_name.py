# Generated by Django 5.0.1 on 2024-04-24 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_qr_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qr_data',
            name='event_name',
        ),
        migrations.RemoveField(
            model_name='qr_data',
            name='name',
        ),
    ]
