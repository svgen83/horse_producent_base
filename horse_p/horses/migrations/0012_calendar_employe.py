# Generated by Django 3.2.18 on 2023-12-05 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0011_auto_20231205_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='employe',
            field=models.ManyToManyField(related_name='action', to='horses.Employee'),
        ),
    ]
