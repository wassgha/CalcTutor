from django.contrib import admin

from .models import Course, Topic, Exercise

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Exercise)
