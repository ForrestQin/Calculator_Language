from abst import *
from tokenizer import tokenize


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
			left = BinaryOperation(left, operator, right)

		return left

	def parse_multiplicative(self):
		left = self.parse_exponentiation()

		while self.tokens[self.index].type == "OPERATOR" and self.tokens[self.index].value in ("*", "/", "%"):
			operator = self.tokens[self.index].value
			self.index += 1
			right = self.parse_exponentiation()
			left = BinaryOperation(left, operator, right)

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
			raise ValueError("Mismatched parentheses")
		elif self.index < len(self.tokens) and self.tokens[self.index].type == "COMMA":
			self.index += 1
			return self.parse_primary()
		else:
			raise ValueError("Invalid expression")

	def parse_exponentiation(self):
		left = self.parse_unary()

		while self.tokens[self.index].type == "OPERATOR" and self.tokens[self.index].value == "^":
			operator = self.tokens[self.index].value
			self.index += 1
			right = self.parse_unary()
			left = BinaryOperation(left, operator, right)

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

		if self.tokens[self.index].type == "IDENTIFIER":
			var_name = self.tokens[self.index].value
			self.index += 1

			if self.tokens[self.index].type == "OPERATOR":
				operator = self.tokens[self.index].value
				if operator == "=":
					self.index += 1
					expr_parser = ExpressionParser(self.tokens[self.index:])
					expr = expr_parser.parse()
					self.index += expr_parser.index
					return Assignment(var_name, expr)
				elif operator == "++":
					self.index += 1
					return PostIncrement(Variable(var_name))
				elif operator == "--":
					self.index += 1
					return PostDecrement(Variable(var_name))

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

		raise ValueError("Invalid statement")


def parse_code(code):
	tokens = tokenize(code)
