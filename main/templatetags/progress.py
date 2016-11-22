from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Sum
from main.models import Attempt, Exercise

register = template.Library()
@register.assignment_tag
def exercise_progress(user, exercise):
	num_correct = Attempt.objects.filter(user = user, exercise=exercise, correct=True).count()
	return 0 if num_correct is None else (100*num_correct)/exercise.question_count

@register.assignment_tag
def topic_progress(user, topic):
	topic_question_count = Exercise.objects.filter(topic = topic, exercise_active = True).aggregate(Sum('question_count'))['question_count__sum']
	if topic_question_count is None:
		return 0
	num_correct = Attempt.objects.filter(user = user, exercise__in=topic.exercise_set.filter(exercise_active = True), correct=True).count()
	return 0 if num_correct is None else (100*num_correct)/topic_question_count