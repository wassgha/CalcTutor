class QuestionData(object):
	def __init__(self, tree, funcString, secondString, domain, eval_table):
		self.tree = tree
		self.funcString = funcString
		self.derivString = secondString
		self.integralString = secondString
		self.domain = domain
		self.eval_table = eval_table