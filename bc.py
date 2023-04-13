import sys

from abst import PrintStatement
from tokenizer import tokenize
from expressionAndStatementParser import StatementParser, DivideByZeroError, ParseError
from evaluator import Evaluator


def main():
	evaluator = Evaluator()

	all_tokens = []
	print_statements = []

	try:
		while True:
			line = input() + "\n"
			tokens = tokenize(line)
			all_tokens.extend(tokens)

			parser = StatementParser(tokens)
			try:
				statements = parser.parse()
			except ValueError as e:
				print(e)
				continue
			except Exception as e:
				print(f"Unexpected error: {e}")
				continue

			for statement in statements:
				result = evaluator.evaluate(statement)
				if isinstance(statement, PrintStatement):
					print_statements.append(result)

	except EOFError:
		for statement in print_statements:
			print(statement)

if __name__ == "__main__":
	main()
