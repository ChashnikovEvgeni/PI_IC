"""Accounting_table URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from IC.views import index, IndicatorViewSet, auth
from django.urls import path, include

#router = SimpleRouter()    #это djangorestframework  унести потом

#router.register(r'Indicator', IndicatorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('IC/', include('IC.urls')),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('__debug__/', include('debug_toolbar.urls')),

#разнести потом всё по urls
]

if settings.DEBUG:
    import debug_toolbar
    import mimetypes

    mimetypes.add_type("IC/javascript", ".js", True)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

def show_toolbar(request):
    return True
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

#urlpatterns += router.urls
