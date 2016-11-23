from django.contrib import admin

from .models import Course, Topic, Exercise, Attempt

class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'question', 'question_num', 'answer', 'correct', 'submit_date')


admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Exercise)
admin.site.register(Attempt, AttemptAdmin)
