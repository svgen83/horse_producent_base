# Generated by Django 3.2.18 on 2023-12-07 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0021_auto_20231207_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab_group',
            name='employees',
            field=models.ManyToManyField(related_name='serviced_group', to='horses.Employee'),
        ),
    ]
