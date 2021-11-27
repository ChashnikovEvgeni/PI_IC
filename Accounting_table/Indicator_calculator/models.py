from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=255)
    target_indicator_IUC = models.DecimalField(max_digits=5, decimal_places=2)
    actual_indicator_IUC = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # list_of_departmentst

class Department(models.Model):
    title = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    #List_of_indicators
    #Уточнить название перемнной, фактический или плановый
    PPRTD_weight = models.DecimalField(max_digits=5, decimal_places=4)
    PFVIR_weight = models.DecimalField(max_digits=5, decimal_places=4)
    department_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0)

class Indicator(models.Model):
    title = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    comment = models.TextField()
    target_indicator = models.DecimalField(max_digits=4, decimal_places=1)
    actual_indicator = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    Significance_of_indicator = models.DecimalField(max_digits=5, decimal_places=4)
    Plan = models.DecimalField(max_digits=4, decimal_places=1)
    Degree_of_compliance = models.DecimalField(max_digits=4, decimal_places=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)