
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_id>[0-9])$', views.course_page, name='course_page'),
]
