class ASTNode:
	def __str__(self):
		return self.__class__.__name__

	def children(self):
		return []

	def to_string(self, indent=0):
		result = " " * indent + str(self) + "\n"
		for child in self.children():
			result += child.to_string(indent + 2)
		return result


class Expression(ASTNode):
	pass


class Number(Expression):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return f"{self.__class__.__name__}({self.value})"


class Variable(Expression):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return f"{self.__class__.__name__}({self.name})"


class BinaryOperation(Expression):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

	def __str__(self):
		return f"{self.__class__.__name__}({self.operator})"

	def children(self):
		return [self.left, self.right]


class UnaryOperation(Expression):
	def __init__(self, operator, operand):
		self.operator = operator
		self.operand = operand

	def __str__(self):
		return f"{self.__class__.__name__}({self.operator})"

	def children(self):
		return [self.operand]


class FunctionCall(Expression):
	def __init__(self, name, arguments):
		self.name = name
		self.arguments = arguments

	def __str__(self):
		return f"{self.__class__.__name__}({self.name})"

	def children(self):
		return self.arguments


class PreIncrement(Expression):
	def __init__(self, variable):
		self.variable = variable


class PreDecrement(Expression):
	def __init__(self, variable):
		self.variable = variable


class PostIncrement(Expression):
	def __init__(self, variable):
		self.variable = variable


class PostDecrement(Expression):
	def __init__(self, variable):
		self.variable = variable


class Statement(ASTNode):
	pass


class Assignment(Statement):
	def __init__(self, variable, expression):
		self.variable = variable
		self.expression = expression

	def __str__(self):
		return f"{self.__class__.__name__}({self.variable})"

	def children(self):
		return [self.expression]


class Print(Statement):
	def __init__(self, expressions):
		self.expressions = expressions

	def children(self):
		return self.expressions


class IfStatement(Statement):
	def __init__(self, condition, then_block, else_block=None):
		self.condition = condition
		self.then_block = then_block
		self.else_block = else_block

	def children(self):
		if self.else_block:
			return [self.condition, self.then_block, self.else_block]
		return [self.condition, self.then_block]


class WhileStatement(Statement):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body

	def children(self):
		return [self.condition, self.body]


class FunctionDefinition(Statement):
	def __init__(self, name, arguments, body):
		self.name = name
		self.arguments = arguments
		self.body = body

	def __str__(self):
		return f"{self.__class__.__name__}({self.name})"

	def children(self):
		return self.arguments + [self.body]


class Return(Statement):
	def __init__(self, expression=None):
		self.expression = expression

	def children(self):
		if self.expression:
			return [self.expression]
		return []


class PrintStatement(Statement):
	def __init__(self, expressions):
		self.expressions = expressions

	def __str__(self):
		return f"{self.__class__.__name__}"

	def children(self):
		return self.expressions
