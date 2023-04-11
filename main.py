import sys
from tokenizer import tokenize
from parser import StatementParser
from evaluator import Evaluator


def main():
	evaluator = Evaluator()

	print("Enter your commands, one per line. Press Ctrl-D (Unix) or Ctrl-Z (Windows) to exit.")
	all_tokens = []

	try:
		while True:
			line = input("> ")
			tokens = tokenize(line + "\n")
			all_tokens.extend(tokens)

			parser = StatementParser(tokens)
			statements = parser.parse()

			for statement in statements:
				evaluator.evaluate(statement)
	except EOFError:
		print("\nExiting...")


if __name__ == "__main__":
	main()
