
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_id>[0-9])$', views.course, name='course'),
    url(r'^course/(?P<course_id>[0-9])/topic/(?P<topic_id>[0-9])$', views.topic, name='topic'),
    url(r'^course/(?P<course_id>[0-9])/topic/(?P<topic_id>[0-9])/exercise/(?P<exercise_id>[0-9])$', views.exercise, name='exercise'),
]
