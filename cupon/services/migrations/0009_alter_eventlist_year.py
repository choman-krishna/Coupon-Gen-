# Generated by Django 5.0.1 on 2024-04-23 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_eventlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlist',
            name='year',
            field=models.CharField(default='2023', max_length=4),
        ),
    ]
