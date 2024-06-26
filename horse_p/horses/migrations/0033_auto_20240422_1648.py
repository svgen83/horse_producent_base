# Generated by Django 3.2.18 on 2024-04-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horses', '0032_alter_lab_group_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='restriction',
            name='begin_restriction',
            field=models.DateField(blank=True, default='2024-01-01', verbose_name='дата начала действия ограничения'),
        ),
        migrations.AddField(
            model_name='restriction',
            name='end_restriction',
            field=models.DateField(blank=True, default='2024-01-01', verbose_name='дата завершения действия ограничения'),
        ),
    ]
