import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from FunctionTree import *
from Production import *
from random import choice, randint, uniform
from steps import diffsteps
from django.contrib.sessions.backends.db import SessionStore
from latex2sympy.process_latex import process_sympy


class Question(object):

	"""
	
	Exercise parameters

	"""
	input_method = "MathKeyboard"

	"""

	Initialize the exercise (generate a function)

	"""

	def __init__(self, key, new):
		session = SessionStore(session_key=key)
		#session.clear()
		print key
		print session.items()
		if 'derivString' not in session or new:
			tree = FunctionTree.buildTreeWithMaxComplexity(0)
			func =  tree.getOutputFunction()
			deriv =  tree.getOutputDerivative() 
			session['funcString'] = func.toString()
			session['derivString'] = deriv.toString()
			session.save()
		self.funcString =  session['funcString']
		self.derivString =  session['derivString']
		# print "Derivative : " 
		#print self.tree.getOutputDerivative()
		self.eval_table = [(x, parse_expr(self.derivString).subs(symbols("x"),  x)) for x in np.arange(-10, 10, 0.5)]


	"""

	getPrompt() returns the text of the question in HTML.

	"""

	def getPrompt(self):
		prompt = "<p>Differentiate this function : </p><br>"
		# self.tree.printTree()
		# diffsteps.print_html_steps(randfn, Symbol('x'))
		prompt += "<script type=\"math/tex; mode=display\">" + latex(parse_expr(self.funcString)) + "</script>"
		# prompt += "<br><table><tr><td>x</td><td>y</td></tr>"
		# for(x, y) in self.eval_table:
		# 	try:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>" + str(y) + "</td></tr>"
		# 	except:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>Division by zero</td></tr>"

		# prompt += "</table>"
		prompt += "<div id='solution'><p>Solution : </p><br>"
		prompt += "<script type=\"math/tex; mode=display\">" + latex(simplify(parse_expr(self.derivString))) + "</script></div>"
		return prompt

	"""

	getAnswer() evaluates the student's answer and returns "correct" or hints.

	"""

	def getAnswer(self, studentInput):
		if studentInput=='': 
			return ''
		answer = process_sympy(studentInput.replace('\\right', '').replace('\\left', ''))
		answer_eval_table = [(x, answer.subs(symbols("x"),  x)) for x in np.arange(-10, 10, 0.5)]

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
		if self.eval_table == answer_eval_table:
			result+="Correct!"
			return result
		else:
			result+="Incorrect answer, try again."
			return result