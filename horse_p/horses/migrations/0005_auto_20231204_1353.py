# Generated by Django 3.2.18 on 2023-12-04 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0004_auto_20231204_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manipulation',
            name='manipulation_date',
        ),
        migrations.AlterField(
            model_name='calendar',
            name='manipulations',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.DO_NOTHING, related_name='manipulation_date', to='horses.manipulation'),
        ),
    ]
