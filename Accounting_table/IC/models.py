import sys

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse


class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    indicator_RTD = models.DecimalField(max_digits=5, decimal_places=2, default= 0)
    indicator_VIR = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from IC.logic import set_indicators_RTD_VIR
        set_indicators_RTD_VIR(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Служба(уточнить название раздела)'
        verbose_name_plural = 'Служба(уточнить название раздела)'
        ordering = ['title']

class Department(models.Model):
    title = models.TextField(verbose_name="Название")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    #List_of_indicators
    #Уточнить название перемнной, фактический или плановый
    department_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Показатель")
    PPRTD_weight = models.DecimalField(max_digits=5, decimal_places=4, default= 0, verbose_name="Вес, приоритет передача режимно- технологических данных") # вес, приоритет передача режимно- технологических данных
    PPRTD_indicator = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="ППРТД Показатель")
    PFVIR_weight = models.DecimalField(max_digits=5, decimal_places=4, default= 0, verbose_name="Вес, приоритет функционирование ВИР") # вес, приоритет функционирование ВИР
    PFVIR_indicator = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="ПФВИР Показатель")

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from IC.logic import set_department_indicator
        set_department_indicator(self)
        super().save(*args, **kwargs)
        Service.objects.get(id=self.service.id).save()

    class Meta:
        verbose_name = 'Отделы/группы'
        verbose_name_plural = 'Отделы/группы'
        ordering = ['service', 'title']


class Indicator(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    units = models.CharField(max_length=255, verbose_name="Единицы измерения")
    comment = models.TextField(verbose_name="Комментарий")
    #задали заранее
    target_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Целевой показатель")
    #фактическое значение
    actual_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Фактический показатель")
    #вес показателя
    Significance_of_indicator = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Вес показателя")
    Plan = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="План")
    # в excel значение показателя за отчётный период
    Degree_of_compliance = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="Выполнение")
    #
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    # персчёт коэффициента соответствия при каждом изменении

    def get_absolute_url(self):
        return reverse('indicator-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from IC.logic import set_Degree_of_compliance
        set_Degree_of_compliance(self)
        super().save(*args, **kwargs)
        Department.objects.get(id=self.department.id).save()

    class Meta:
        verbose_name = 'Показатели'
        verbose_name_plural = 'Показатели'
        ordering = ['department', 'title']



class Critical_service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    working_mode_days = models.DecimalField(max_digits=1, decimal_places=0, default=0, null=True, verbose_name="Рабочих дней в неделю")
    working_mode_hours = models.DecimalField(max_digits=2, decimal_places=0, default=0, null=True, verbose_name="Рабочих часов в день")
    working_days_period = models.DecimalField(max_digits=2, decimal_places=0, default=0, null=True, verbose_name="Рабочих дней в отчётном периоде")
    Operating_time_plan = models.DecimalField(max_digits=4, decimal_places=0, default=0, null=True, verbose_name="План, ч")
    Operating_time_actual = models.DecimalField(max_digits=4, decimal_places=0, default=0, null=True, verbose_name="Факт, ч")
    Completion_rate = models.DecimalField(max_digits=4, decimal_places=3, default=0, null=True, verbose_name="Выполнение")
    Service_ownership = models.CharField(max_length=255, verbose_name="Принадлежность")

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def get_absolute_url(self):
        return reverse('critical_service-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        from IC.logic import set_operating_time
        set_operating_time(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Критически важные сервисы/службы'
        verbose_name_plural = 'Критически важные сервисы/службы'
        ordering = ['title']
#@receiver(pre_save, sender=Indicator)
#def set_Degees(sender, instance, **kwargs):
 #   from IC.logic import set_Degree_of_compliance
  #  instance.Degree_of_compliance = set_Degree_of_compliance(instance)
