# Generated by Django 3.2.18 on 2023-08-01 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Antigen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Наименование материала для иммунизации')),
                ('description_short', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('description_long', models.TextField(blank=True, verbose_name='Подробное описание')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Фамилия, имя, отчество')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение')),
                ('laboratory', models.CharField(max_length=200, verbose_name='Структурное подразделение')),
                ('duties', models.TextField(blank=True, verbose_name='Должноcтные обязанности')),
            ],
        ),
        migrations.CreateModel(
            name='Equine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='Кличка лошади')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='изображение')),
                ('anamnesis', models.TextField(blank=True, default='', verbose_name='Анамнез')),
                ('date_of_birth', models.DateField(verbose_name='дата рождения')),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='дата смерти')),
                ('commissioning_date', models.DateField(verbose_name='дата ввода в эксплутацию')),
            ],
        ),
        migrations.CreateModel(
            name='Manipulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название манипуляции')),
                ('description', models.TextField(blank=True, verbose_name='Описание манипуляции')),
                ('manipulation_date', models.DateField(verbose_name='дата осуществления манипуляции')),
            ],
        ),
    ]
