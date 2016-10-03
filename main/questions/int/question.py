import numpy as np
import types

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
		print key
		#session.clear()
		self.domain = 2*np.random.random(60)
		if 'integralString' not in session or new:
			self.generateFunction()
			while len(self.eval_table) < 10:
				self.generateFunction()
			session['funcString'] = self.funcString
			session['integralString'] = self.integralString
			session.save()
		else:
			self.funcString = session['funcString']
			self.integralString = session['integralString']
			self.generateDerivEvalTable()
		self.tree = None

		print session.items()
	def generateFunction(self):
		tree = FunctionTree.buildTreeWithMaxComplexity(4)
		tree.printTree()
		func =  tree.getOutputFunction()
		integral =  tree.getOutputIntegral()
		self.funcString = func.toString()
		self.integralString = integral.toString()
		self.generateDerivEvalTable()

	def generateDerivEvalTable(self) :
		self.eval_table = np.array([(x, Function.evaluate(self.integralString, x)) for x in self.domain if isinstance(Function.evaluate(self.integralString, x), Float)]).astype(float)

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
		prompt = "<p>Integrate this function : </p><br>"
		# diffsteps.print_html_steps(randfn, Symbol('x'))
		prompt += "<script type=\"math/tex; mode=display\">" + self.postprocessSym2Lat(latex(parse_expr(self.funcString))) + "</script>"
		# prompt += "<br><table><tr><td>x</td><td>y</td></tr>"
		# for(x, y) in self.eval_table:
		# 	try:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>" + str(y) + "</td></tr>"
		# 	except:
		# 		prompt += "<tr><td>" + str(x) + "</td><td>Division by zero</td></tr>"

		# prompt += "</table>"
		prompt += "<div id='solution'><p>Solution : </p><br>"
		prompt += "<script type=\"math/tex; mode=display\">" + self.postprocessSym2Lat(latex(parse_expr(self.integralString))) + "</script></div>"
		return prompt

	"""

	getAnswer() evaluates the student's answer and returns "correct" or hints.

	"""

	def getAnswer(self, studentInput):
		if studentInput=='':
			return ''
		answer = process_sympy(self.preprocessLat2Sym(studentInput))
		#answer_eval_table = np.array([(x, N(answer.subs(symbols("x"),  x))) for x in self.domain if isinstance(N(answer.subs(symbols("x"),  x)), Float)]).astype(float)
		answer_eval_table = np.array([(x, N(answer.subs(symbols("x"),  x))) for x in self.domain if isinstance(N(answer.subs(symbols("x"),  x)), Float)]).astype(float)

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
		#
		# Tolerance values are currently set with no real justification, but hopefully are generous enough at least
		if self.eval_table.shape == answer_eval_table.shape and np.allclose(self.eval_table, answer_eval_table, rtol=1e-02, atol=1e-05):
			result+="Correct!"
			return result
		else:
			result+="Incorrect answer, try again."
			return result
