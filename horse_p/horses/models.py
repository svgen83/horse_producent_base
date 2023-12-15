from django.db import models

# Create your models here.


class Antigen(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Наименование материала для иммунизации')
    description_short = models.TextField(
        'Краткое описание', blank=True)
    description_long = models.TextField(
        'Подробное описание', blank=True)
    production_date = models.DateField(
        verbose_name='дата приготовления',
        blank=True, null = True)
    
    class Meta:
        verbose_name = 'Антиген'
        verbose_name_plural = 'Антигены'
        ordering = ['title']
    def __str__(self):
        return self.title


class Manipulation(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Название манипуляции')
    description = models.TextField('Описание манипуляции',
                                   blank=True)
    volume = models.CharField(max_length=200,
                              verbose_name='Объем, мл',
                              blank = "True")
    class Meta:
        verbose_name = 'Тип манипуляции'
        verbose_name_plural = 'Типы манипуляций'
        ordering = ['title']
                                         
    def __str__(self):
        return self.title


class Employee(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Фамилия, имя, отчество')
    image = models.ImageField(verbose_name='изображение',
                              upload_to='media',
                              blank=True, null=True
                              )
    laboratory = models.CharField('Структурное подразделение', max_length=200)
    job_title = models.TextField('Должноcть', blank=True)
    duties = models.TextField('Должноcтные обязанности', blank=True)
    manipulate_acts = models.ManyToManyField(Manipulation, related_name='employees')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['title']

    def __str__(self):
        return self.title


class Lab_group(models.Model):
    title = models.IntegerField(verbose_name='название группы')

    antigen = models.ForeignKey(Antigen, on_delete = models.DO_NOTHING,
                                related_name="antigen_group",
                                blank = True, null = True,
                                verbose_name='Используемый материал для иммунизации' )
    employees = models.ManyToManyField(Employee,
                                 related_name='serviced_group')
    def employee_names(self):
        return u" %s" % (u", ".join([employee.title for employee in self.employees.all()]))
    employee_names.short_description = u'Ответственные сотрудники'


    class Meta:
        verbose_name = 'Лабораторная группа'
        verbose_name_plural = 'Лабораторные группы'
        ordering = ['title']
    def __str__(self):
        return str(self.title)



class Equine(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,
                             verbose_name='Кличка')
    sex = models.CharField(max_length=200,
                           verbose_name='Пол',
                           blank=True, null=True)
    image = models.ImageField(verbose_name='изображение',
                              upload_to='media',
                              blank=True, null=True
                              )
    anamnesis = models.TextField(verbose_name='Анамнез',
                                 blank=True, default='')
    date_of_birth = models.DateField(verbose_name='дата рождения')
    date_of_death = models.DateField(verbose_name='дата выбытия',
                                     blank=True, null=True)
    commissioning_date = models.DateField(verbose_name='дата ввода в эксплутацию')
    lab_group = models.ForeignKey(Lab_group,
                                  on_delete = models.DO_NOTHING,
                                  related_name='equine',
                                  blank = 'True', null = 'True',
                                  verbose_name='Лабораторная группа')

    class Meta:
        verbose_name = 'Лошадь-продуцент'
        verbose_name_plural = 'Лошади-продуценты'
        ordering = ['lab_group', 'title']

    def __str__(self):
        return self.title 


class Calendar(models.Model):
       
    date_manipulation = models.DateField(
        verbose_name='дата проведения манипуляции')
    groups = models.ForeignKey(Lab_group,
                               on_delete = models.DO_NOTHING,
                               verbose_name='Рабочая группа',
                               blank = 'True', null = 'True')
    manipulations = models.ForeignKey(Manipulation,
                                      on_delete = models.DO_NOTHING,
                                      blank = 'True', null = 'True',
                                      related_name='manipulation_date')
    employe = models.ManyToManyField(Employee,
                                     verbose_name='Исполнители',
                                     related_name='action')

    class Meta:
        verbose_name = 'Дата проведения процедуры'
        verbose_name_plural = 'Даты проведения процедуры'
        ordering = ['date_manipulation', 'groups']
    
    def get_category(self):
        return ",".join([str(item) for item in self.employe.all()])
    get_category.short_description = u'Ответственные сотрудники'

    def __str__(self):
        return str(self.date_manipulation)


class Restriction(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Названия ограничений')
    reason = models.TextField(verbose_name='Описание причины ограничения',
                              blank=True, default='')
    equine = models.ManyToManyField(Equine,
                                    verbose_name='Кличка лошади',
                                    related_name="restriction_to_use")
    class Meta:
        verbose_name = 'Ограничение по эксплуатации'
        verbose_name_plural = 'Ограничения по эксплуатации'
        ordering = ['title']
    

class Cure(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Названия метода лечения')
    reason = models.TextField(verbose_name='Описание способа лечения',
                              blank=True, default='')
    equine = models.ForeignKey(Equine,
                               on_delete = models.DO_NOTHING,
                               related_name='prescribed_treatment')
    therapist = models.ForeignKey(Employee,
                                  on_delete = models.DO_NOTHING,
                                  related_name='therapist')

    class Meta:
        verbose_name = 'Лечение'
        verbose_name_plural = 'Лечение'
        ordering = ['title']










