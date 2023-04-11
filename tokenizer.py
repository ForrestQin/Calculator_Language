import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value"])

TOKEN_TYPES = [
    ("NUMBER", r"\d+(\.\d*)?"),
    ("KEYWORD", r"\bprint\b"),
    ("OPERATOR", r"\+\+|--|[\+\-*/%^=()]"),
    ("NEWLINE", r"\n"),
    ("COMMA", r","),
    ("IDENTIFIER", r"[a-zA-Z]\w*"),
    ("WHITESPACE", r"[ \t]+"),
]



# def tokenize(code):
#     tokens = []
#     index = 0
#
#     while index < len(code):
#         char = code[index]
#
#         if char.isspace():
#             index += 1
#             continue
#
#         if char.isdigit() or char == '.':
#             number_start = index
#             while index < len(code) and (code[index].isdigit() or code[index] == '.'):
#                 index += 1
#             tokens.append(Token("NUMBER", code[number_start:index]))
#             continue
#
#         if char.isalpha() or char == '_':
#             identifier_start = index
#             while index < len(code) and (code[index].isalnum() or code[index] == '_'):
#                 index += 1
#             identifier = code[identifier_start:index]
#
#             if identifier in KEYWORDS:
#                 tokens.append(Token("KEYWORD", identifier))
#             else:
#                 tokens.append(Token("IDENTIFIER", identifier))
#             continue
#
#         if char == ',':
#             tokens.append(Token("COMMA", char))
#             index += 1
#             continue
#
#         if char in OPERATORS:
#             tokens.append(Token("OPERATOR", char))
#             index += 1
#             continue
#
#         if char == '\n':
#             tokens.append(Token("NEWLINE", char))
#             index += 1
#             continue
#
#         raise ValueError(f"Invalid character: {char}")
#
#     return tokens

def tokenize(code):
    token_pattern = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKEN_TYPES))
    return [
        Token(match.lastgroup, match.group(match.lastgroup))
        for match in token_pattern.finditer(code)
        if match.lastgroup != "WHITESPACE"
    ]