from __future__ import unicode_literals

from django.db import models


class Course(models.Model):
	course_name = models.CharField(max_length=200)
	course_desc = models.CharField(max_length=200)
	course_color = models.CharField(max_length=200)
	def short_course_desc(self):
		return self.course_desc[:100] + "..." if len(self.course_desc)>=100 else self.course_desc
	def shorter_course_desc(self):
		return self.course_desc[:50] + "..." if len(self.course_desc)>=50 else self.course_desc
	def short_course_name(self):
		return self.course_name[:20] + "..." if len(self.course_name)>=20 else self.course_name
	# pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.course_name

class Topic(models.Model):
	topic_name = models.CharField(max_length=200)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	def __str__(self):
		return self.topic_name

class Exercise(models.Model):
	exercise_name = models.CharField(max_length=200)
	file_name = models.CharField(max_length=200)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	def __str__(self):
		return self.exercise_name

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
