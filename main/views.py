from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Course, Topic, Exercise
from .utils import *

from .forms import AnswerForm


import sys, os

# Create your views here.

def index(request):
	courses = Course.objects.all()
	context = {
		'courses': courses,
	}
	return render(request, 'index.html', context)

def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course.html', {
        'course': course,
		# 'rand_fn': "$" + latex(randfn) + "$",
		# 'diff': "$" + latex(diff(randfn)) + "$",
		# 'integral': "$" + latex(integrate(randfn)) + "$"

    })

def topic(request, course_id, topic_id):
    course = get_object_or_404(Course, pk=course_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'topic.html', {
        'progressRange': range(0, 100),
        'course': course,
        'topic': topic,
    })


def exercise(request, course_id, topic_id, exercise_id):
    course = get_object_or_404(Course, pk=course_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    
    answer=''
    new = False

    if request.method == 'POST':
	    form = AnswerForm(request.POST)
	    new = True if 'new' in form.data else False
	    if form.is_valid():
	        answer = form.cleaned_data['answer']
    else:
        form = AnswerForm()

    sys.path.append(os.path.join(os.path.dirname(__file__), 'questions/' + exercise.file_name))
    import question
    quest = question.Question(request.session.session_key, new)



    # randfn = rand_fn()
    return render(request, 'exercise.html', {
        'course': course,
        'topic': topic,
        'prompt': quest.getPrompt(),
        'answer': quest.getAnswer(answer),
        'input_method': quest.input_method,
        'exercise': exercise,
        'form' : form
   		# 'rand_fn': latex(randfn),
		# 'diff': latex(diff(randfn)),
		# 'diff_steps': diffsteps.print_html_steps(randfn, Symbol('x')),
		# 'integral': "$" + latex(integrate(randfn)) + "$"

    })