import re

# Define token specifications
token_specification = [
    ("NUMBER",   r'\d+(\.\d*)?'),     # Integer or decimal number
    ("ID",       r'[A-Za-z_]\w*'),    # Identifiers
    ("ASSIGN",   r'='),               # Assignment operator
    ("END",      r';'),               # Statement terminator
    ("OP",       r'[+\-*/]'),         # Arithmetic operators
    ("COMPARE",  r'[<>!]=|[<>]'),     # Comparison operators
    ("LPAREN",   r'\('),              # Left Parenthesis
    ("RPAREN",   r'\)'),              # Right Parenthesis
    ("LBRACE",   r'\{'),              # Left Brace
    ("RBRACE",   r'\}'),              # Right Brace
    ("NEWLINE",  r'\n'),              # Line endings
    ("SKIP",     r'[ \t]+'),          # Skip spaces and tabs
    ("MISMATCH", r'.'),               # Any other character
]

# Predefined keywords
keywords = {"if", "else", "while", "for", "int", "float", "return", "print"}

# Build the regex pattern
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def lexer(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
            tokens.append((kind, value))
        elif kind == "ID":
            if value in keywords:
                tokens.append(("KEYWORD", value))
            else:
                tokens.append((kind, value))
        elif kind == "NEWLINE" or kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character {value!r}")
        else:
            tokens.append((kind, value))
    return tokens


if __name__ == "__main__":
    # Sample source code
    source_code = """
    int x = 10;
    float y = 20.5;
    if (x < y) {
        print(x + y);
    }
    """

    print("Source Code:")
    print(source_code)
    print("\nTokens:")
    for token in lexer(source_code):
        print(token)
