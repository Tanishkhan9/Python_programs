import re

# ---------------- Lexer ----------------
token_specification = [
    ("NUMBER",   r'\d+(\.\d*)?'),
    ("ID",       r'[A-Za-z_]\w*'),
    ("PLUS",     r'\+'),
    ("MINUS",    r'-'),
    ("MUL",      r'\*'),
    ("DIV",      r'/'),
    ("LPAREN",   r'\('),
    ("RPAREN",   r'\)'),
    ("SKIP",     r'[ \t]+'),
    ("MISMATCH", r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def lexer(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
            tokens.append(("NUMBER", value))
        elif kind == "ID":
            tokens.append(("ID", value))
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character {value!r}")
        else:
            tokens.append((kind, value))
    tokens.append(("EOF", None))
    return tokens

# ---------------- Parser ----------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def parse(self):
        return self.expr()

    # Grammar:
    # expr → term ((PLUS | MINUS) term)*
    def expr(self):
        node = self.term()
        while self.current_token[0] in ("PLUS", "MINUS"):
            op = self.current_token
            self.eat(op[0])
            right = self.term()
            node = ("BIN_OP", op, node, right)
        return node

    # term → factor ((MUL | DIV) factor)*
    def term(self):
        node = self.factor()
        while self.current_token[0] in ("MUL", "DIV"):
            op = self.current_token
            self.eat(op[0])
            right = self.factor()
            node = ("BIN_OP", op, node, right)
        return node

    # factor → NUMBER | ID | LPAREN expr RPAREN
    def factor(self):
        token = self.current_token
        if token[0] == "NUMBER":
            self.eat("NUMBER")
            return ("NUMBER", token[1])
        elif token[0] == "ID":
            self.eat("ID")
            return ("ID", token[1])
        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node
        else:
            raise SyntaxError(f"Unexpected token {token}")

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    source_code = "a + 3 * (b - 2)"
    
    print("Source Code:", source_code)
    
    tokens = lexer(source_code)
    print("\nTokens:")
    print(tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\nAbstract Syntax Tree (AST):")
    print(ast)
