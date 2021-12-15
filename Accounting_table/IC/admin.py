from django.contrib import admin

from .models import Indicator, Department, Service

admin.site.register(Indicator)
admin.site.register(Department)
admin.site.register(Service)
# Register your models here.
