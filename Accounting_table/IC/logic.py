from IC.models import Indicator, Department


def set_Degree_of_compliance(indicator):
    degree_of_compliance = indicator.actual_indicator / indicator.Plan * 100
    indicator.Degree_of_compliance = degree_of_compliance



def set_department_indicator(department):
    department.department_indicator = 0
    for i in Indicator.objects.filter(department=department):
        department.department_indicator +=  i.Significance_of_indicator * i.actual_indicator / i.Plan * 100
    department.PPRTD_indicator = department.department_indicator*department.PPRTD_weight
    department.PFVIR_indicator = department.department_indicator*department.PFVIR_weight



def set_indicators_RTD_VIR(service):
    service.indicator_RTD = 0
    service.indicator_VIR = 0
    for d in Department.objects.filter(service=service):
        service.indicator_RTD += d.PPRTD_indicator
        service.indicator_VIR += d.PFVIR_indicator

def set_operating_time(critical_service):
    critical_service.Operating_time_actual = critical_service.working_days_period * critical_service.working_mode_hours
    critical_service.Completion_rate = round(critical_service.Operating_time_actual / critical_service.Operating_time_plan, 3)