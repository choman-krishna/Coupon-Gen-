# Generated by Django 5.0.1 on 2024-04-23 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_service_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=20)),
                ('date', models.CharField(max_length=2)),
                ('month', models.CharField(max_length=10)),
                ('year', models.CharField(max_length=4)),
            ],
        ),
    ]