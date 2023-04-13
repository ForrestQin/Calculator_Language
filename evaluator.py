from abst import *
from expressionAndStatementParser import DivideByZeroError, ErrorStatement


class Evaluator:
	def __init__(self):
		self.variables = {}
		self.functions = {}

	def evaluate(self, node):
		if isinstance(node, ErrorStatement):
			return node.error
		elif isinstance(node, Number):
			return node.value

		elif isinstance(node, Variable):
			return self.variables.get(node.name, 0.0)


		elif isinstance(node, PreIncrement):
			value = self.variables.get(node.variable.name, 0.0) + 1
			self.variables[node.variable.name] = value
			return value

		elif isinstance(node, PreDecrement):
			value = self.variables.get(node.variable.name, 0.0) - 1
			self.variables[node.variable.name] = value
			return value

		elif isinstance(node, PostIncrement):
			value = self.variables.get(node.variable.name, 0.0)
			self.variables[node.variable.name] = value + 1
			return value

		elif isinstance(node, PostDecrement):
			value = self.variables.get(node.variable.name, 0.0)
			self.variables[node.variable.name] = value - 1
			return value

		elif isinstance(node, BinaryOperation):
			left = self.evaluate(node.left)
			right = self.evaluate(node.right)

			if node.operator == '+':
				return left + right
			elif node.operator == '-':
				return left - right
			elif node.operator == '*':
				return left * right
			elif node.operator == '/':
				if right == 0:
					return "divide by zero"
				return left / right
			elif node.operator == '^':
				return left ** right
		# Add more operators as needed

		elif isinstance(node, UnaryOperation):
			operand = self.evaluate(node.operand)

			if node.operator == '-':
				return -operand
		# Add more unary operators as needed

		elif isinstance(node, FunctionCall):
			function = self.functions.get(node.name)
			if function is None:
				raise ValueError(f"Undefined function: {node.name}")

			if len(node.arguments) != len(function.parameters):
				raise ValueError(f"Argument count mismatch for function {node.name}")
			previous_variables = self.variables.copy()
			for param, arg in zip(function.parameters, node.arguments):
				self.variables[param.name] = self.evaluate(arg)
			return_value = 0.0

			for statement in function.body:

				result = self.evaluate(statement)

				if isinstance(statement, Return):
					return_value = result

					break

			# Restore the previous state of the variables

			self.variables = previous_variables

			return return_value

		elif isinstance(node, Statement):
			if isinstance(node, Assignment):
				value = self.evaluate(node.expression)
				self.variables[node.variable] = value
				return value

			elif isinstance(node, IfStatement):
				condition = self.evaluate(node.condition)
				if condition != 0:
					for statement in node.if_body:
						self.evaluate(statement)
				else:
					for statement in node.else_body:
						self.evaluate(statement)

			elif isinstance(node, WhileStatement):
				while self.evaluate(node.condition) != 0:
					for statement in node.body:
						self.evaluate(statement)


			elif isinstance(node, FunctionDefinition):
				self.functions[node.name] = node
				return None

			elif isinstance(node, Return):
				return self.evaluate(node.expression)
			# worked 1
			# elif isinstance(node, PrintStatement):
			# 	results = [self.evaluate(expr) for expr in node.expressions]
			# 	print(" ".join(str(result) for result in results))
			# 	return None
			elif isinstance(node, PrintStatement):
				results = [self.evaluate(expr) for expr in node.expressions]
				return " ".join(str(result) for result in results)
		else:
			raise ValueError(f"Unknown node type: {node}")

		def evaluate_statement(self, statement):
			try:
				return self.evaluate(statement), None
			except DivideByZeroError as e:
				return None, str(e)
