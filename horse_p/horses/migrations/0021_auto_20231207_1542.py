# Generated by Django 3.2.18 on 2023-12-07 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0020_auto_20231205_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='employe',
            field=models.ManyToManyField(related_name='action', to='horses.Employee', verbose_name='Исполнители'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='groups',
            field=models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.DO_NOTHING, to='horses.lab_group', verbose_name='Рабочая группа'),
        ),
    ]