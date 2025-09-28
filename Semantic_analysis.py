import re

# ---------------- Lexer ----------------
token_specification = [
    ("NUMBER",   r'\d+(\.\d*)?'),
    ("ID",       r'[A-Za-z_]\w*'),
    ("ASSIGN",   r'='),
    ("PLUS",     r'\+'),
    ("MINUS",    r'-'),
    ("MUL",      r'\*'),
    ("DIV",      r'/'),
    ("SEMI",     r';'),
    ("LPAREN",   r'\('),
    ("RPAREN",   r'\)'),
    ("TYPE",     r'int|float'),
    ("SKIP",     r'[ \t\n]+'),
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
        elif kind in ("ID", "TYPE"):
            tokens.append((kind, value))
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
        statements = []
        while self.current_token[0] != "EOF":
            statements.append(self.statement())
        return ("PROGRAM", statements)

    def statement(self):
        if self.current_token[0] == "TYPE":  # Declaration
            type_token = self.current_token
            self.eat("TYPE")
            var_name = self.current_token
            self.eat("ID")
            self.eat("SEMI")
            return ("DECL", type_token[1], var_name[1])
        elif self.current_token[0] == "ID":  # Assignment
            var_name = self.current_token
            self.eat("ID")
            self.eat("ASSIGN")
            expr_node = self.expr()
            self.eat("SEMI")
            return ("ASSIGN", var_name[1], expr_node)
        else:
            raise SyntaxError(f"Invalid statement: {self.current_token}")

    # Grammar: expr → term ((PLUS | MINUS) term)*
    def expr(self):
        node = self.term()
        while self.current_token[0] in ("PLUS", "MINUS"):
            op = self.current_token
            self.eat(op[0])
            right = self.term()
            node = ("BIN_OP", op[1], node, right)
        return node

    # term → factor ((MUL | DIV) factor)*
    def term(self):
        node = self.factor()
        while self.current_token[0] in ("MUL", "DIV"):
            op = self.current_token
            self.eat(op[0])
            right = self.factor()
            node = ("BIN_OP", op[1], node, right)
        return node

    # factor → NUMBER | ID | ( expr )
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

# ---------------- Semantic Analyzer ----------------
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # var_name → type

    def analyze(self, node):
        node_type = node[0]

        if node_type == "PROGRAM":
            for stmt in node[1]:
                self.analyze(stmt)

        elif node_type == "DECL":
            _, var_type, var_name = node
            if var_name in self.symbol_table:
                raise Exception(f"Semantic Error: Redeclaration of variable '{var_name}'")
            self.symbol_table[var_name] = var_type

        elif node_type == "ASSIGN":
            _, var_name, expr = node
            if var_name not in self.symbol_table:
                raise Exception(f"Semantic Error: Undeclared variable '{var_name}'")
            expr_type = self.evaluate_expr(expr)
            var_type = self.symbol_table[var_name]

            if var_type == "int" and expr_type == "float":
                raise Exception(f"Semantic Error: Cannot assign float to int variable '{var_name}'")

        elif node_type == "BIN_OP":
            return self.evaluate_expr(node)

    def evaluate_expr(self, node):
        node_type = node[0]

        if node_type == "NUMBER":
            return "float" if isinstance(node[1], float) else "int"
        elif node_type == "ID":
            var_name = node[1]
            if var_name not in self.symbol_table:
                raise Exception(f"Semantic Error: Undeclared variable '{var_name}'")
            return self.symbol_table[var_name]
        elif node_type == "BIN_OP":
            _, op, left, right = node
            left_type = self.evaluate_expr(left)
            right_type = self.evaluate_expr(right)

            if left_type == "float" or right_type == "float":
                return "float"
            return "int"

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    source_code = """
    int x;
    float y;
    x = 5;
    y = x + 2.5;
    z = 10;   // Error: undeclared variable
    """

    print("Source Code:")
    print(source_code)

    tokens = lexer(source_code)
    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAbstract Syntax Tree (AST):")
    print(ast)

    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(ast)
        print("\nSemantic Analysis: PASSED ✅")
        print("Symbol Table:", analyzer.symbol_table)
    except Exception as e:
        print("\nSemantic Analysis: FAILED ❌")
        print(e)
