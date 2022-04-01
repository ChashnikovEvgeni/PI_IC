import sys

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.backends import django
from django.urls import reverse


class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    indicator_RTD = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="ППРТД показатель")
    indicator_VIR = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="ПФВИР показатель")

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})

# для пересчёта итогового показателя службы
    def save(self, *args, **kwargs):
        from IC.logic import set_indicators_RTD_VIR
        set_indicators_RTD_VIR(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Служба(уточнить название раздела)'
        verbose_name_plural = 'Службы(уточнить название раздела)'
        ordering = ['title']


class Department(models.Model):
    title = models.TextField(verbose_name="Название")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="Служба")
    # List_of_indicators
    # Уточнить название перемнной, фактический или плановый
    department_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Показатель")
    PPRTD_weight = models.DecimalField(max_digits=5, decimal_places=4, default=0,
                                       verbose_name="Вес, приоритет передача режимно- технологических данных")  # вес, приоритет передача режимно- технологических данных
    PPRTD_indicator = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="ППРТД Показатель")
    PFVIR_weight = models.DecimalField(max_digits=5, decimal_places=4, default=0,
                                       verbose_name="Вес, приоритет функционирование ВИР")  # вес, приоритет функционирование ВИР
    PFVIR_indicator = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="ПФВИР Показатель")

    def __str__(self):
        return f'  {self.title}'

    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})

    # для пересчёта итогового показателя отдела/группы
    def save(self, *args, **kwargs):
        from IC.logic import set_department_indicator
        set_department_indicator(self)
        super().save(*args, **kwargs)
        Service.objects.get(id=self.service.id).save()

    class Meta:
        verbose_name = 'Отдел/группа'
        verbose_name_plural = 'Отделы/группы'
        ordering = ['service', 'title']


class Indicator(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    units = models.CharField(max_length=255, verbose_name="Единицы измерения", null=True)
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    target_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Целевой показатель")
    actual_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0,
                                           verbose_name="Фактический показатель")
    Significance_of_indicator = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Вес показателя")
    Plan = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="План")
    Degree_of_compliance = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Выполнение")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, verbose_name="отдел/группа")

    # Confirmation_document = models.FileField(upload_to="documents/", null=True, verbose_name="Подтверждающий документ")

    def __str__(self):
        return f'Id {self.id}: {self.title}'



    def get_absolute_url(self):
        return reverse('indicator-detail', kwargs={'pk': self.pk})

    # персчёт коэффициента соответствия при каждом изменении
    def save(self, *args, **kwargs):
        from IC.logic import set_Degree_of_compliance
        set_Degree_of_compliance(self)
        super().save(*args, **kwargs)
        Department.objects.get(id=self.department.id).save()

    class Meta:
        verbose_name = 'Показатель'
        verbose_name_plural = 'Показатели'
        ordering = ['department', 'title']


class Indicators_file(models.Model):
    confirmation_document = models.FileField(upload_to="documents/", null=True, verbose_name="Подтверждающие документы")
    date_of_download = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки документа")
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True, verbose_name="Показатель")

    def __str__(self):
        return f'Id {self.confirmation_document}'

    def get_absolute_url(self):
        return reverse('indicators_file-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Подтверждающий документ'
        verbose_name_plural = 'Подтверждающие документы'


class Critical_service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    working_mode_days = models.DecimalField(max_digits=1, decimal_places=0, default=0, null=True,
                                            verbose_name="Рабочих дней в неделю")
    working_mode_hours = models.DecimalField(max_digits=2, decimal_places=0, default=0, null=True,
                                             verbose_name="Рабочих часов в день")
    working_days_period = models.DecimalField(max_digits=2, decimal_places=0, default=0, null=True,
                                              verbose_name="Рабочих дней в отчётном периоде")
    Operating_time_plan = models.DecimalField(max_digits=4, decimal_places=0, default=0, null=True,
                                              verbose_name="План, ч")
    Operating_time_actual = models.DecimalField(max_digits=4, decimal_places=0, default=0, null=True,
                                                verbose_name="Факт, ч")
    Completion_rate = models.DecimalField(max_digits=4, decimal_places=3, default=0, null=True,
                                          verbose_name="Выполнение")
    Service_ownership = models.CharField(max_length=255, verbose_name="Принадлежность")

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse('critical_service-detail', kwargs={'pk': self.pk})

     # пересчёт времени при изменении и добавлении объекта в базе
    def save(self, *args, **kwargs):
        from IC.logic import set_operating_time
        set_operating_time(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Критически важные сервисы/службы'
        verbose_name_plural = 'Критически важные сервисы/службы'
        ordering = ['title']


