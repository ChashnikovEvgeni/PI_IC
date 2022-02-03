from django.contrib import admin

from IC.models import Indicator, Department, Service, Critical_service



class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department_indicator', 'PPRTD_weight', 'PPRTD_indicator', 'PFVIR_weight', 'PFVIR_indicator')
    search_fields = ('title',)

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('id','title','units', 'comment', 'target_indicator', 'actual_indicator', 'Significance_of_indicator', 'Plan', 'Degree_of_compliance' )
    search_fields = ('title',)

class Critical_serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','working_mode_days', 'working_mode_hours', 'working_days_period', 'Operating_time_plan', 'Operating_time_actual', 'Completion_rate', 'Service_ownership' )
    search_fields = ('title',)


admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Service)
admin.site.register(Critical_service, Critical_serviceAdmin)
# Register your models here.
