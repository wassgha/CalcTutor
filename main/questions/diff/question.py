import numpy as np
import types
import sys, os
import pickle

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from django.contrib.sessions.backends.db import SessionStore
sys.path.append(os.path.abspath(os.path.dirname(__name__)))
from main.static.latex2sympy.process_latex import process_sympy
from main.question_factory.DiffProd import FunctionTree, Production, Function
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
		if 'diff' not in session:
			session['diff'] = {}
		if 'questionNum' not in session['diff']:
			session['diff']['questionNum'] = 0
			session.save()
		elif new:
			session['diff']['questionNum'] = session['diff']['questionNum'] + 1
			session.save()
		questionFileName = "../../../main/question_factory/diff/generated_questions/difficulty" + str(self.difficulty) + "_" + str(session['diff']['questionNum']) + ".question"
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
		prompt = "<p>Differentiate this function : </p>"
		# diffsteps.print_html_steps(randfn, Symbol('x'))
		prompt += "<script type=\"math/tex; mode=display\">" + self.postprocessSym2Lat(latex(parse_expr(self.question.funcString))) + "</script>"
		# prompt += "<br><table><tr><td>x</td><td>y</td></tr>"
		# for(x, y) in self.question.eval_table:
		# 	try:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>" + str(y) + "</td></tr>"
		# 	except:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>Division by zero</td></tr>"

		# prompt += "</table>"
		prompt += "<div id='solution'><p>Solution : </p><br>"
		prompt += "<script type=\"math/tex; mode=display\">" + self.postprocessSym2Lat(latex(parse_expr(self.question.derivString))) + "</script></div>"
		return prompt

	"""

	getAnswer() evaluates the student's answer and returns "correct" or hints.

	"""

	def getAnswer(self, studentInput):
		if studentInput=='':
			return ''
		answer = process_sympy(self.preprocessLat2Sym(studentInput))
		#answer_eval_table = np.array([(x, N(answer.subs(symbols("x"),  x))) for x in self.question.domain if isinstance(N(answer.subs(symbols("x"),  x)), Float)]).astype(float)
		answer_eval_table = np.array([(x, N(answer.subs(symbols("x"),  x))) for x in self.question.domain if isinstance(N(answer.subs(symbols("x"),  x)), Float)]).astype(float)

		# print("The output function is: ")
		# print(func.toString())
		# print("The value of the output function for x = 5 is: ")
		# print(func.evaluate(5))
		# print("Which is approximately: " )
		# print(N(func.evaluate(5)))
		result=""
		# result += "<br><table><tr><td>x</td><td>y</td></tr>"
		# for(x, y) in answer_eval_table:
		# 	try:
		# 		result += "<tr><td>" + str(x) + "</td><td>" + str(y) + "</td></tr>"
		# 	except:
		# 		result += "<tr><td>" + str(x) + "</td><td>Division by zero</td></tr>"

		# result += "</table>"
		
		# Tolerance values are currently set with no real justification, but hopefully are generous enough at least
		if self.question.eval_table.shape == answer_eval_table.shape and np.allclose(self.question.eval_table, answer_eval_table, rtol=1e-02, atol=1e-05):
			result+="Correct!"
			return result
		else:
			result+="Incorrect answer, try again."
			return result
