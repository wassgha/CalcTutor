import numpy as np
import types
import sys, os
import pickle

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from django.contrib.sessions.backends.db import SessionStore
sys.path.append(os.path.abspath(os.path.dirname(__name__)))
from main.static.latex2sympy.process_latex import process_sympy
from main.question_factory.IntProd import IntFunctionTree, IntProduction, Function
from main.question_factory.QuestionData import QuestionData


class Question(object):

	"""

	Exercise parameters

	"""
	input_method = "MathKeyboard"
	difficulty = 4
	dirname = "generated_questions"


	"""

	Initialize the exercise

	"""

	def __init__(self, key, new):
		session = SessionStore(session_key=key)
		if 'int' not in session:
			session['int'] = {}
		if 'questionNum' not in session['int']:
			session['int']['questionNum'] = 0
			session.save()
		elif new:
			self.isCorrect = False
			session['int']['questionNum'] = session['questionNum'] + 1
			session.save()
		questionFileName = "../../../main/question_factory/int/generated_questions/difficulty" + str(self.difficulty) + "_" + str(session['questionNum']) + ".question"
		with open(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), questionFileName)), 'rb') as questionFile:
			self.question = pickle.load(questionFile)

	def preprocessLat2Sym(self, string):
		return (string.replace('\\right', '')
		.replace('\\left', '')
		.replace("^x","^{(x)}")
		.replace("\ ","")
		)

	def postprocessSym2Lat(self, string):
		return (string.replace('\\log ','\\ln ')
		.replace('\\log{','\\ln{')
		)


	"""

	getPrompt() returns the text of the question in HTML.

	"""

	def getPrompt(self):
		prompt = "<p>Integrate this function : </p>"
		# diffsteps.print_html_steps(randfn, Symbol('x'))
		prompt += "<script type=\"math/tex; mode=display\">" + self.postprocessSym2Lat(latex(parse_expr(self.question.funcString))) + "</script>"
		# prompt += "<br><table><tr><td>x</td><td>y</td></tr>"
		# for(x, y) in self.eval_table:
		# 	try:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>" + str(y) + "</td></tr>"
		# 	except:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>Division by zero</td></tr>"

		# prompt += "</table>"
		prompt += "<div id='solution'><p>Solution : </p><br>"
		prompt += "<script type=\"math/tex; mode=display\">" + self.postprocessSym2Lat(latex(parse_expr(self.question.integralString))) + "</script></div>"
		return prompt

	"""

	getAnswer() evaluates the student's answer and returns true if correct and false otherwise.

	"""

	def getAnswer(self, studentInput):
		if studentInput=='':
			return ''
		answer = process_sympy(self.preprocessLat2Sym(studentInput))
		#Differentiate student input
		answer_derivative = process_sympy("\\frac{d{" + self.preprocessLat2Sym(studentInput) + "}}{dx}")

		answer_eval_table = np.array([(x, N(answer_derivative.subs(symbols("x"),  x))) for x in self.domain if isinstance(N(answer_derivative.subs(symbols("x"),  x)), Float)]).astype(float)

		return self.question.eval_table.shape == answer_eval_table.shape and np.allclose(self.question.eval_table, answer_eval_table, rtol=1e-02, atol=1e-05)

	def getMessage(self, answer):
		if answer:
			return '<div class="alert alert-success" role="alert"><strong>Correct answer!</strong> Click next to conitnue</div>'
		else:
			return '<div class="alert alert-danger" role="alert"><strong>Incorrect answer.</strong> see <a href="#">a hint</a>?</div>'