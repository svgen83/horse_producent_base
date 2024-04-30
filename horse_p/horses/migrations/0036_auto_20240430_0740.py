# Generated by Django 3.2.18 on 2024-04-30 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0035_alter_lab_group_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='manipulate_acts',
            field=models.ManyToManyField(blank=True, related_name='employees', to='horses.Manipulation'),
        ),
        migrations.AlterField(
            model_name='lab_group',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='serviced_group', to='horses.Employee'),
        ),
    ]