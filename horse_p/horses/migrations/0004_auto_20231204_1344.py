# Generated by Django 3.2.18 on 2023-12-04 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0003_alter_lab_group_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='groups',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.DO_NOTHING, to='horses.lab_group'),
            preserve_default='True',
        ),
        migrations.AddField(
            model_name='calendar',
            name='manipulations',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.DO_NOTHING, to='horses.manipulation'),
            preserve_default='True',
        ),
    ]