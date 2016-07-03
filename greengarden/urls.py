from django.conf.urls import url

from . import views


app_name = 'greengarden'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cuestionario/$', views.cuestionario, name='cuestionario'),
]