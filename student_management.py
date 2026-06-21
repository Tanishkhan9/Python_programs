students = {}

while True:

    print("\n1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":

        roll = input("Roll No: ")
        name = input("Name: ")

        students[roll] = name

        print("Student Added")

    elif choice == "2":

        for roll, name in students.items():
            print(roll, "-", name)

    elif choice == "3":

        roll = input("Enter Roll No: ")

        if roll in students:
            print(students[roll])
        else:
            print("Not Found")

    elif choice == "4":
        break

    else:
        print("Invalid Choice")