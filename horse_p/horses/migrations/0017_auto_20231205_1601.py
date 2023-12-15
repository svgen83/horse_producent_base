# Generated by Django 3.2.18 on 2023-12-05 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0016_auto_20231205_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lab_group',
            name='employee',
        ),
        migrations.AddField(
            model_name='employee',
            name='serviced_group',
            field=models.ManyToManyField(blank='True', null='True', related_name='served_officers', to='horses.Lab_group'),
            preserve_default='True',
        ),
    ]
