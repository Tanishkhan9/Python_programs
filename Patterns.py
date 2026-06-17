# Pattern Printing using Match-Case (Python 3.10+)

choice = int(input("""
Choose Pattern:
1. Square
2. Right Triangle
3. Pyramid
4. Inverted Triangle

Enter Choice: """))

rows = int(input("Enter Number of Rows: "))

match choice:

    case 1:
        print("\nSquare Pattern")
        for i in range(rows):
            print("* " * rows)

    case 2:
        print("\nRight Triangle")
        for i in range(1, rows + 1):
            print("* " * i)

    case 3:
        print("\nPyramid Pattern")
        for i in range(rows):
            print(" " * (rows - i - 1) + "* " * (i + 1))

    case 4:
        print("\nInverted Triangle")
        for i in range(rows, 0, -1):
            print("* " * i)

    case _:
        print("Invalid Choice")
