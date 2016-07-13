from django.conf.urls import url

from . import views


app_name = 'greengarden'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cuestionario/$', views.cuestionario, name='cuestionario'),
    url(r'^conclusion/(?P<hecho_id>[0-9]+)/$', views.conclusion, name='conclusion'),
    url(r'^inferir/$', views.inferir, name='inferir')
]