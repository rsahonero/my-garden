from django.conf.urls import url

from . import views


app_name = 'greengarden'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cuestionario/$', views.cuestionario, name='cuestionario'),
    url(r'^conclusion/(?P<task_id>[^/]+)/$', views.conclusion, name='conclusion'),
    url(r'^inferir/$', views.inferir, name='inferir'),
    url(r'^actualizar/$', views.actualizar, name='actualizar')
]