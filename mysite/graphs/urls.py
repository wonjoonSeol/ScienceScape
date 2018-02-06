from django.urls import path

from . import views

urlpatterns = [
    url('^$', views.index, name='index')
]
