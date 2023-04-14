import sys

from abst import PrintStatement
from tokenizer import tokenize
from parse import StatementParser, ErrorStatement, ParseError
from evaluate import Evaluator


def main():
	evaluator = Evaluator()

	all_tokens = []
	print_statements = []

	
	while True:
		try:
			line = input() + "\n"
			tokens = tokenize(line)
			all_tokens.extend(tokens)

			parser = StatementParser(tokens)
			try:
				statements = parser.parse()

				for statement in statements:
					result = evaluator.evaluate(statement)
					if isinstance(statement, PrintStatement):
						print_statements.append(result)
						print(result)
					elif isinstance(result, ErrorStatement):
						print('divide by zero')
			except ParseError:
				print('parse error')
				continue
		except EOFError:
			break


if __name__ == "__main__":
	main()
