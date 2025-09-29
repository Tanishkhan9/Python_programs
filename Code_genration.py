class CodeGenerator:
    def __init__(self, tac):
        self.tac = tac
        self.assembly = []

    def generate(self):
        for line in self.tac:
            lhs, rhs = line.split("=")
            lhs = lhs.strip()
            rhs = rhs.strip()
            tokens = rhs.split()

            # Case 1: Direct assignment (x = 5, x = y)
            if len(tokens) == 1:
                if tokens[0].isdigit():
                    self.assembly.append(f"PUSH {tokens[0]}")
                else:
                    self.assembly.append(f"LOAD {tokens[0]}")
                self.assembly.append(f"STORE {lhs}")

            # Case 2: Binary operation (t1 = a + b)
            elif len(tokens) == 3:
                a, op, b = tokens
                # Load left operand
                if a.isdigit():
                    self.assembly.append(f"PUSH {a}")
                else:
                    self.assembly.ap
