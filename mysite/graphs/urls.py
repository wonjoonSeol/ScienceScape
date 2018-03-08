from django.conf.urls import url

from . import views

urlpatterns = [
<<<<<<< HEAD
   # path('graphs/', include('graphs.urls')),
   # path('admin/', admin.site.urls),
=======
    url('^$', views.index, name='index')
>>>>>>> master
]
