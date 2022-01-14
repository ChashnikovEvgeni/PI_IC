import sys

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver



class Service(models.Model):
    title = models.CharField(max_length=255)
    indicator_RTD = models.DecimalField(max_digits=5, decimal_places=2, default= 0)
    indicator_VIR = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def save(self, *args, **kwargs):
        from IC.logic import set_indicators_RTD_VIR
        set_indicators_RTD_VIR(self)
        super().save(*args, **kwargs)

class Department(models.Model):
    title = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    #List_of_indicators
    #Уточнить название перемнной, фактический или плановый
    department_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    PPRTD_weight = models.DecimalField(max_digits=5, decimal_places=4, default= 0) # вес, приоритет передача режимно- технологических данных
    PPRTD_indicator = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    PFVIR_weight = models.DecimalField(max_digits=5, decimal_places=4, default= 0) # вес, приоритет функционирование ВИР
    PFVIR_indicator = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    def save(self, *args, **kwargs):
        from IC.logic import set_department_indicator
        set_department_indicator(self)
        super().save(*args, **kwargs)
        Service.objects.get(id=self.service.id).save()


class Indicator(models.Model):
    title = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    comment = models.TextField()
    #задали заранее
    target_indicator = models.DecimalField(max_digits=4, decimal_places=1, default= 0)
    #фактическое значение
    actual_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    #вес показателя
    Significance_of_indicator = models.DecimalField(max_digits=5, decimal_places=4)
    Plan = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    # в excel значение показателя за отчётный период
    Degree_of_compliance = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    #
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    # персчёт коэффициента соответствия при каждом изменении

    def save(self, *args, **kwargs):
        from IC.logic import set_Degree_of_compliance
        set_Degree_of_compliance(self)
        super().save(*args, **kwargs)
        Department.objects.get(id=self.department.id).save()



    @property
    def same(self):
        self.Plan = self.actual_indicator - self.target_indicator
        return self.Plan


#@receiver(pre_save, sender=Indicator)
#def set_Degees(sender, instance, **kwargs):
 #   from IC.logic import set_Degree_of_compliance
  #  instance.Degree_of_compliance = set_Degree_of_compliance(instance)
