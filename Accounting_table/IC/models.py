from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=255)
    target_indicator_IUC = models.DecimalField(max_digits=5, decimal_places=2, default= 0)
    actual_indicator_IUC = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # list_of_departmentst
    def __str__(self):
        return f'Id {self.id}: {self.title}'


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


class Indicator(models.Model):
    title = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    comment = models.TextField()
    target_indicator = models.DecimalField(max_digits=4, decimal_places=1, default= 0)
    actual_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    Significance_of_indicator = models.DecimalField(max_digits=5, decimal_places=4)
    Plan = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    Degree_of_compliance = models.DecimalField(max_digits=4, decimal_places=1, default= 0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    @property
    def same(self):
        self.Plan = self.actual_indicator - self.target_indicator
        return self.Plan