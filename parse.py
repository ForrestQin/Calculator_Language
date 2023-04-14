from abst import *
from tokenizer import *


class ExpressionParser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.index = 0

	def parse(self):
		return self.parse_additive()

	def parse_additive(self):
		left = self.parse_multiplicative()

		while self.tokens[self.index].type == "OPERATOR" and self.tokens[self.index].value in ("+", "-"):
			operator = self.tokens[self.index].value
			self.index += 1
			right = self.parse_multiplicative()
			left = LeftOperation(left, operator, right)

		return left


	def parse_multiplicative(self):
		left = self.parse_exponentiation()

		while self.index < len(self.tokens) and self.tokens[self.index].type == "OPERATOR" and self.tokens[
			self.index].value in ("*", "/", "%"):
			operator = self.tokens[self.index].value
			self.index += 1
			if self.index == len(self.tokens) or self.tokens[self.index].type == "NEWLINE":
				raise ParseError("parse error")
			right = self.parse_exponentiation()
			left = LeftOperation(left, operator, right)
		return left

	def parse_unary(self):
		if self.tokens[self.index].type == "OPERATOR" and self.tokens[self.index].value in ("++", "--", "-"):
			operator = self.tokens[self.index].value
			self.index += 1
			if operator == "++":
				variable = self.parse_primary()
				return PreIncrement(variable)
			elif operator == "--":
				variable = self.parse_primary()
				return PreDecrement(variable)
			else:  # operator == "-"
				operand = self.parse_unary()
				return UnaryOperation(operator, operand)
		return self.parse_primary()

	def parse_primary(self):
		token = self.tokens[self.index]
		if token.type == "NUMBER":
			self.index += 1
			return Number(float(token.value))
		elif token.type == "IDENTIFIER":
			self.index += 1
			if self.index < len(self.tokens) and self.tokens[self.index].type == "OPERATOR":
				operator = self.tokens[self.index].value
				if operator == "++":
					self.index += 1
					return PostIncrement(Variable(token.value))
				elif operator == "--":
					self.index += 1
					return PostDecrement(Variable(token.value))
			return Variable(token.value)
		elif token.type == "OPERATOR" and token.value == "(":
			self.index += 1
			expression = self.parse_additive()
			if self.index < len(self.tokens) and self.tokens[self.index].type == "OPERATOR" and self.tokens[
				self.index].value == ")":
				self.index += 1
				return expression
			raise ParseError("parse error")
		elif self.index < len(self.tokens) and self.tokens[self.index].type == "COMMA":
			self.index += 1
			return self.parse_primary()
		elif token.type == "OPERATOR" and token.value != "(":
			raise ParseError("parse error")
		else:
			raise ParseError("parse error")

	def parse_exponentiation(self):
		left = self.parse_unary()

		while self.tokens[self.index].type == "OPERATOR" and self.tokens[self.index].value == "^":
			operator = self.tokens[self.index].value
			self.index += 1
			right = self.parse_unary()
			left = RightOperation(left, operator, right)

		return left


class StatementParser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.index = 0

	def parse(self):
		statements = []

		while self.index < len(self.tokens):
			statement = self.parse_statement()
			if statement:
				statements.append(statement)

		return statements

	def parse_statement(self):
		if self.tokens[self.index].type == "NEWLINE":
			self.index += 1
			return None

		if self.tokens[self.index].type == "NUMBER" or self.tokens[self.index].type == "IDENTIFIER":
			expr_parser = ExpressionParser(self.tokens[self.index:])
			expr = expr_parser.parse()
			self.index += expr_parser.index

			if self.tokens[self.index].type == "OPERATOR":
				operator = self.tokens[self.index].value
				if operator == "=":
					if self.tokens[self.index - expr_parser.index].type == "IDENTIFIER":
						var_name = self.tokens[self.index - expr_parser.index].value
						self.index += 1
						expr_parser = ExpressionParser(self.tokens[self.index:])
						# print(self.tokens[self.index:])
						expr = expr_parser.parse()
						self.index += expr_parser.index
						return Assignment(var_name, expr)
					else:
						raise ParseError("parse error")
				elif operator in ["+=", "-=", "*=", "/=", "%=", "^="]:
					if self.tokens[self.index - expr_parser.index].type == "IDENTIFIER":
						var_name = self.tokens[self.index - expr_parser.index].value
						self.index += 1
						tokens = [Token('IDENTIFIER', var_name), Token('OPERATOR', operator[0])] + self.tokens[self.index:]
						expr_parser = ExpressionParser(tokens)
						expr = expr_parser.parse()
						self.index += expr_parser.index
						return Assignment(var_name, expr)
					else:
						raise ParseError("parse error")
				elif operator == "++":
					self.index += 1
					return PostIncrement(expr)
				elif operator == "--":
					self.index += 1
					return PostDecrement(expr)
				else:
					raise ParseError("parse error")
			else:
				return expr

		elif self.tokens[self.index].type == "OPERATOR" and self.tokens[self.index].value in ("++", "--"):
			operator = self.tokens[self.index].value
			self.index += 1

			if self.tokens[self.index].type == "IDENTIFIER":
				var_name = self.tokens[self.index].value
				self.index += 1

				if operator == "++":
					return PreIncrement(Variable(var_name))
				elif operator == "--":
					return PreDecrement(Variable(var_name))

		elif self.tokens[self.index].type == "KEYWORD" and self.tokens[self.index].value == "print":
			self.index += 1
			expressions = []
			while self.tokens[self.index].type != "NEWLINE":
				expr_parser = ExpressionParser(self.tokens[self.index:])
				expressions.append(expr_parser.parse())
				self.index += expr_parser.index
				if self.tokens[self.index].type == "COMMA":
					self.index += 1
			self.index += 1
			return PrintStatement(expressions)
		else:
			raise ParseError()
	def has_next(self):
		return self.index < len(self.tokens)



class ParseError(Exception):
	pass


class DivideByZeroError(Exception):
	pass


class ErrorStatement:
	def __init__(self, error):
		self.error = error

	def __repr__(self):
		return f"ErrorStatement({repr(self.error)})"


def parse_code(code):
	tokens = tokenize(code)