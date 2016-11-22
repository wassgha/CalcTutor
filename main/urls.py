
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_id>[0-9])$', views.course, name='course'),
    url(r'^course/(?P<course_id>[0-9])/topic/(?P<topic_id>[0-9])$', views.topic, name='topic'),
    url(r'^course/(?P<course_id>[0-9])/topic/(?P<topic_id>[0-9])/exercise/(?P<exercise_id>[0-9])$', views.exercise, name='exercise'),
	url(r'^%s$' % settings.LOGIN_URL[1:], auth_views.login, kwargs={'template_name': 'login.html'},  name='auth_login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, 'auth_logout'),

]
