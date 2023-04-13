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


def tokenize(code):
    token_pattern = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKEN_TYPES))
    return [
        Token(match.lastgroup, match.group(match.lastgroup))
        for match in token_pattern.finditer(code)
        if match.lastgroup != "WHITESPACE"
    ]