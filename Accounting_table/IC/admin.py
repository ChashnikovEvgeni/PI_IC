from django.contrib import admin

from IC.models import Indicator, Department, Service, Critical_service, Indicators_file, Profile


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'indicator_RTD', 'indicator_VIR')
    list_display_links = ('id',)
    #list_editable = ('title', 'indicator_RTD', 'indicator_VIR')
    search_fields = ('title',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department_indicator', 'PPRTD_weight', 'PPRTD_indicator', 'PFVIR_weight', 'PFVIR_indicator', 'service')
    list_display_links = ('id',)
   # list_editable = ('title', 'department_indicator', 'PPRTD_weight', 'PPRTD_indicator', 'PFVIR_weight', 'PFVIR_indicator')
    list_filter = ('id', 'service')
    search_fields = ('title',)


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('id','title','units', 'comment', 'target_indicator', 'actual_indicator', 'Significance_of_indicator', 'Plan', 'Degree_of_compliance', 'department')
    list_display_links = ('id', )
    #list_editable = ('title','units', 'comment', 'target_indicator', 'actual_indicator', 'Significance_of_indicator', 'Plan', 'Degree_of_compliance' )
    list_filter = ('department',)
    search_fields = ('title',)

class Indicators_fileAdmin(admin.ModelAdmin):
    list_display = ('id', 'confirmation_document', 'date_of_download', 'indicator')
    list_display_links = ('id',)
    list_filter = ('indicator',)


class Critical_serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','working_mode_days', 'working_mode_hours', 'working_days_period', 'Operating_time_plan', 'Operating_time_actual', 'Completion_rate', 'Service_ownership' )
    list_display_links = ('id', )
    #list_editable = ('title','working_mode_days', 'working_mode_hours', 'working_days_period', 'Operating_time_plan', 'Operating_time_actual', 'Completion_rate', 'Service_ownership' )
    list_filter = list_display = ('id', 'title','working_mode_days', 'working_mode_hours','Service_ownership' )
    search_fields = ('title',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','position')


admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Indicators_file)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Critical_service, Critical_serviceAdmin)
admin.site.register(Profile, ProfileAdmin)
# Register your models here.
