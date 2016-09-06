from __future__ import unicode_literals

from django.db import models


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_desc = models.CharField(max_length=200)
    course_color = models.CharField(max_length=200)
    def short_course_desc(self):
    	return self.course_desc[:100] + "..." if len(self.course_desc)>=100 else self.course_desc
    # pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.course_name

class Topic(models.Model):
	topic_name = models.CharField(max_length=200)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
