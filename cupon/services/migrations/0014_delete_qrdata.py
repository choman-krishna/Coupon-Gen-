# Generated by Django 5.0.1 on 2024-04-24 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_qrdata_delete_qr_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QrData',
        ),
    ]