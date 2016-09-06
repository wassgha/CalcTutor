from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Course
from .utils import *

# Create your views here.

def index(request):
	courses = Course.objects.all()
	context = {
		'courses': courses,
	}
	return render(request, 'index.html', context)

def course_page(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    randfn = rand_fn()
    return render(request, 'course.html', {
        'course': course,
		# 'rand_fn': "$" + latex(randfn) + "$",
		# 'diff': "$" + latex(diff(randfn)) + "$",
		# 'integral': "$" + latex(integrate(randfn)) + "$"

    })