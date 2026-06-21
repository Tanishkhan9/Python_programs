# Expense Tracker using Dictionary and File Handling

expenses = {}

while True:

    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Save to File")
    print("5. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":

        category = input("Category: ")
        amount = float(input("Amount: "))

        if category in expenses:
            expenses[category] += amount
        else:
            expenses[category] = amount

        print("Expense Added Successfully!")

    elif choice == "2":

        print("\nExpense Summary:")

        if len(expenses) == 0:
            print("No Expenses Found")
        else:
            for category, amount in expenses.items():
                print(f"{category}: ₹{amount}")

    elif choice == "3":

        total = sum(expenses.values())

        print(f"\nTotal Expense = ₹{total}")

    elif choice == "4":

        with open("expenses.txt", "w") as file:

            for category, amount in expenses.items():
                file.write(
                    f"{category}: ₹{amount}\n"
                )

        print("Expenses Saved Successfully!")

    elif choice == "5":

        print("Thank You!")
        break

    else:
        print("Invalid Choice")