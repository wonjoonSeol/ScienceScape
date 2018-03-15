""" mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name = 'home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name = 'home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from graphs import views
from . import converters

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^graphs/$', views.home, name = 'redirectToLoggedIn'),
    url(r'^addFields/(.*)', views.field_form, name = 'fields'),
    url(r'^processGraph/(.*)', views.load_graph, name = 'load_graph'),
    url(r'about/', views.about, name = 'about'),
    url(r'^login/$', auth_views.login, name = 'login'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^admin/', admin.site.urls),
    url(r'^login_on_home/$', views.login_process, name = 'login_on_home'),
    url(r'^account/$', views.account, name = 'account'),
    url(r'^edit/(.*)$', views.edit_fields, name = 'edit'),
    url(r'^delete/(.*)$', views.delete_file, name = 'delete')
]
