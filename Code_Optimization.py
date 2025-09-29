class Optimizer:
    def __init__(self, code):
        self.code = code

    def optimize(self):
        optimized = []
        constants = {}

        for line in self.code:
            # Example line: "t1 = 2 + 3"
            parts = line.split("=")
            lhs = parts[0].strip()
            rhs = parts[1].strip()

            # ---------------- Constant Folding ----------------
            tokens = rhs.split()
            if len(tokens) == 3 and tokens[0].isdigit() and tokens[2].isdigit():
                a, op, b = tokens
                a, b = int(a), int(b)
                if op == "+": val = a + b
                elif op == "-": val = a - b
                elif op == "*": val = a * b
                elif op == "/": val = a // b
                rhs = str(val)
                line = f"{lhs} = {rhs}"
                constants[lhs] = rhs

            # ---------------- Constant Propagation ----------------
            else:
                for var, value in constants.items():
                    if rhs == var:
                        rhs = value
                        line = f"{lhs} = {rhs}"
                    elif rhs.startswith(var + " "):  # var in expression
                        rhs = rhs.replace(var, value)
                        line = f"{lhs} = {rhs}"

            # ---------------- Dead Code Elimination ----------------
            # If a temp variable is assigned but never used later, skip it.
            # (For simplicity, we keep all lines here. Real implementation needs live-variable analysis.)

            optimized.append(line)

        return optimized


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    tac = [
        "t1 = 2 + 3",
        "t2 = t1 * 4",
        "x = t2",
        "y = x + 0",
        "z = y * 1",
    ]

    print("Original TAC:")
    for line in tac:
        print(line)

    optimizer = Optimizer(tac)
    optimized_tac = optimizer.optimize()

    print("\nOptimized TAC:")
    for line in optimized_tac:
        print(line)
