"""horse_p URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path, include
from horses import views, calendar_views
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews

urlpatterns = [
    re_path(r'^horse/(?P<id>\d+)/$', views.horse, name='horse'),
    re_path(r'^group/(?P<title>\d+)/$', views.group, name='group'),
    re_path(r'^statistics/(?P<name>\d+)', views.statistics, name='statistics'),
    path('calendar', views.calendar, name='calendar'),
##    path('statistics', views.statistics, name='statistics'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
##    path('logout/', authViews.LogoutView.as_view(), name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
