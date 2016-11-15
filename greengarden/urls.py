from django.conf.urls import url

from . import views


app_name = 'greengarden'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<codigo>\d+)/$', views.index, name='index'),
    url(r'^cuestionario/$', views.cuestionario, name='cuestionario'),
    url(r'^conclusion/$', views.conclusion, name='conclusion'),
    url(r'^inferir/$', views.inferir, name='inferir'),
    url(r'^evaluar/$', views.evaluar, name='evaluar'),
    url(r'^actualizar/$', views.actualizar, name='actualizar'),
]
