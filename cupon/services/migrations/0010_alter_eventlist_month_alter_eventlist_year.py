# Generated by Django 5.0.1 on 2024-04-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_alter_eventlist_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlist',
            name='month',
            field=models.CharField(default='May', max_length=10),
        ),
        migrations.AlterField(
            model_name='eventlist',
            name='year',
            field=models.CharField(default='2024', max_length=4),
        ),
    ]
