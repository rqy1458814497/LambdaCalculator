# The Lexer


EOF, DOT, SLASH, NAME, LPAREN, RPAREN, = 'EOF', 'DOT', 'SLASH', 'NAME', 'LPAREN', 'RPAREN'


class Token(object):
	'''
		Token class.
	'''
	def __init__(self, t, v):
		self.type = t
		self.value = v

	def __str__(self):
		return 'Token(%s, %r)' % (self.type, self.value)

	__repr__ = __str__


class Lexer(object):
	'''
		Lexer class. Lexical analyzer.
		Methods: 
			__init__(text)
			get_next_token()
	'''
	def __init__(self, text):
		self.text = text
		self.pos = 1
		self.current_char = text[0]

	def advance(self):
		if self.pos == len(self.text):
			self.current_char = ''
		else:
			self.current_char = self.text[self.pos]
			self.pos += 1

	def ingore_whitespace(self):
		while self.current_char.isspace():
			self.advance()

	def get_name(self):
		ans = ''
		while  (self.current_char.isdigit() or
				self.current_char.isalpha() or
				self.current_char == '_'):
			ans = ans + self.current_char
			self.advance()
		return ans

	def get_next_token(self):
		self.ingore_whitespace()
		if not self.current_char:
			return Token(EOF, '')
		elif self.current_char == '\\':
			self.advance()
			return Token(SLASH, '\\')
		elif self.current_char.isalpha() or self.current_char == '_':
			return Token(NAME, self.get_name())
		elif self.current_char == '(':
			self.advance()
			return Token(LPAREN, '(')
		elif self.current_char == ')':
			self.advance()
			return Token(RPAREN, ')')
		elif self.current_char == '.':
			self.advance()
			return Token(DOT, '.')
		else:
			raise SyntaxError('No prase!')
