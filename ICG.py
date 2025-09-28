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

    def expr(self):
        node = self.term()
        while self.current_token[0] in ("PLUS", "MINUS"):
            op = self.current_token
            self.eat(op[0])
            right = self.term()
            node = ("BIN_OP", op[1], node, right)
        return node

    def term(self):
        node = self.factor()
        while self.current_token[0] in ("MUL", "DIV"):
            op = self.current_token
            self.eat(op[0])
            right = self.factor()
            node = ("BIN_OP", op[1], node, right)
        return node

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

# ---------------- Intermediate Code Generator ----------------
class CodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        node_type = node[0]

        if node_type == "PROGRAM":
            for stmt in node[1]:
                self.generate(stmt)
            return self.code

        elif node_type == "DECL":
            # We don’t generate code for declarations in TAC
            return

        elif node_type == "ASSIGN":
            _, var_name, expr = node
            expr_result = self.generate(expr)
            self.code.append(f"{var_name} = {expr_result}")

        elif node_type == "NUMBER":
            return str(node[1])

        elif node_type == "ID":
            return node[1]

        elif node_type == "BIN_OP":
            _, op, left, right = node
            left_res = self.generate(left)
            right_res = self.generate(right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left_res} {op} {right_res}")
            return temp

# ---------------- Example Usage ----------------
if __name__ == "__main__":
    source_code = """
    int x;
    int y;
    x = 5;
    y = x + 3 * (x - 2);
    """

    print("Source Code:")
    print(source_code)

    tokens = lexer(source_code)
    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAbstract Syntax Tree (AST):")
    print(ast)

    generator = CodeGenerator()
    tac = generator.generate(ast)

    print("\nThree-Address Code (TAC):")
    for line in tac:
        print(line)
