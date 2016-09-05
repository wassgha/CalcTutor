from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Course

from random import randint
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

# Create your views here.

def index(request):
	courses = Course.objects.all()
	context = {
		'courses': courses,
	}
	return render(request, 'index.html', context)

def course_page(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course.html', {
        'course': course,
		'rand_fn': "$" + rand_fn() + "$"
    })

def const():
	return randint(1, 10)
def rand_fn():
	z = "z"
	elementfn = [
				lambda x,y: "(" + str(x) + "*" + str(y) + ")",
				lambda x,y: "(" + str(x) + "/" + str(y) + ")",
				lambda x,y: "(" + str(x) + "**" + str(y) + ")",
				lambda x,y: "cos(" + str(x) + ")",
				lambda x,y: "sin(" + str(x) + ")",
				lambda x,y: "tan(" + str(x) + ")",
				lambda x,y: "sec(" + str(x) + ")",
				lambda x,y: "csc(" + str(x) + ")",
				lambda x,y: "cot(" + str(x) + ")",
				lambda x,y: "exp(" + str(x) + ")",
				lambda x,y: "ln(" + str(x) + ")"]
	chaining = [	
				lambda x: "+" + str(x),
				lambda x: "-" + str(x)]
	fn_parts = []
	for i in range(randint(1,4)):
		fn = z
		for i in range(randint(1,3)):
			fn = elementfn[randint(0, len(elementfn)-1)](fn, const())
		fn_parts.append(fn)
	print fn_parts
	fn = fn_parts[0]
	for fn_part in fn_parts[1:]:
		fn += chaining[randint(0, len(chaining)-1)](fn_part)
	return latex(parse_expr(fn))