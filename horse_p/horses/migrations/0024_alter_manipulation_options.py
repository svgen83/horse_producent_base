# Generated by Django 3.2.18 on 2023-12-07 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0023_auto_20231207_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manipulation',
            options={'ordering': ['title'], 'verbose_name': 'Тип манипуляции', 'verbose_name_plural': 'Типы манипуляций'},
        ),
    ]