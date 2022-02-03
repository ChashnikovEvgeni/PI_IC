from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()  # это djangorestframework

router.register(r'Department', DepartmentViewSet)
router.register(r'Service', ServiceViewSet)
router.register(r'Indicator', IndicatorViewSet)
router.register(r'Critical_service', Critical_serviceViewSet)

urlpatterns = [
    path('', index, name='home'),
    path('allI/', all_Indicators, name='allI'),
    path('allD/', all_Departments, name='allD'),
    path('allS/', all_Service, name='allS')
]

urlpatterns += router.urls

print(urlpatterns)