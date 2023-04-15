import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value"])

TOKEN_TYPES = [
	("NUMBER", r"\d+(\.\d*)?"),
	("KEYWORD", r"\bprint\b"),
	("IDENTIFIER", r"[a-zA-Z]\w*"),
	("WHITESPACE", r"[ \t]+"),
	("SINGLE_COMMENT", r"#.*"),
	("MULTI_COMMENT", r"/\*.*?\*/"),
	("NEWLINE", r"\n"),
	("COMMA", r","),
	("OPERATOR", r"\+\+|--|\+=|\-=|\*=|/=|%=|\^=|==|<=|>=|\!=|<|>|[\+\-*/%^=()]|&&|\|\||!"),
]

IsComment = False


def tokenize(code):
	# Remove multiline comments
	global IsComment
	if code.find("/*") == -1 and code.find("*/") == -1 and IsComment:
		return []
	if code.find("/*") != -1:
		line = str(code)
		index = code.find("/*")
		code = code[:index]
		if line.find("*/") != -1:
			index = line.find("*/")
			right = line[index + 2:]
			code = code + right
		else:
			IsComment = True
	elif code.find("*/") != -1:
		index = code.find("*/")
		code = code[index + 2:]
		IsComment = False
	if code.find("#") != -1:
		index = code.find("#")
		code = code[:index]

	token_pattern = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKEN_TYPES))
	return [
		Token(match.lastgroup, match.group(match.lastgroup))
		for match in token_pattern.finditer(code)
		if match.lastgroup != "WHITESPACE" and match.lastgroup != "SINGLE_COMMENT"
	]
