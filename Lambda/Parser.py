# Parser
from Lexer import *


class LambdaExpr(object):
	'''
		Class of lambda expression.
		Just a base class.
	'''
	pass


class Var(LambdaExpr):
	'''
		A variable in lambda expression
		e.g. x
	'''
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return 'Var(%r)' % (self.name)

	__repr__ = __str__


class Lambda(LambdaExpr):
	'''
		A lambda in lambda expression.
		e.g. (\\x. x)
	'''
	def __init__(self, var, expr):
		self.var = var
		self.expr = expr

	def __str__(self):
		return 'Lambda(%s, %s)' % (self.var, self.expr)

	__repr__ = __str__


class Apply(LambdaExpr):
	'''
		A apply expression in lambda expression.
		e.g. (x y), ((x y) z)
	'''
	def __init__(self, func, arg):
		self.func = func
		self.arg = arg

	def __str__(self):
		return 'Apply(%s, %s)' % (self.func, self.arg)

	__repr__ = __str__


class Parser(object):
	'''
		Parser.
		Methods:
			__init__(text)
			parse()
	'''
	def __init__(self, text):
		self.lexer = Lexer('(' + text + ')')
		self.current_token = self.lexer.get_next_token()

	def eat(self, ty):
		if self.current_token.type != ty:
			raise SyntaxError('Invaild syntax!')
		self.current_token = self.lexer.get_next_token()

	def parse(self):
		'''
			parse the text.
		'''
		stack = []
		last = []
		paren_depth = 0
		while self.current_token.type != EOF:
			token = self.current_token
			if token.type == LPAREN:
				self.eat(LPAREN)
				paren_depth += 1
				stack.append(last)
				last = []
			elif token.type == RPAREN:
				self.eat(RPAREN)
				if not paren_depth:
					raise SyntaxError(
						'Unclosed parentheses: cannot find the matching "(".')
				elif not last:
					raise SyntaxError('Empty parentheses!')
				elif type(last[-1]) == Lambda and last[-1].expr == None:
					raise SyntaxError('Empty lambda!')
				tmp = []
				while last:
					cur = last.pop()
					if type(cur) == Lambda and cur.expr == None:
						ans = tmp.pop()
						while tmp: ans = Apply(ans, tmp.pop())
						cur.expr = ans
					tmp.append(cur)
				ans = tmp.pop()
				while tmp: ans = Apply(ans, tmp.pop())
				last = stack.pop()
				last.append(ans)
			elif token.type == SLASH:
				self.eat(SLASH)
				var = self.current_token
				self.eat(NAME)
				self.eat(DOT)
				last.append(Lambda(var.value, None))
			else:
				var = self.current_token
				self.eat(NAME)
				last.append(Var(var.value))
		return last[0]
