from bank import Bank
from ui import line, create_account_ui, login_ui


def main():
    bank = Bank()
    while True:
        line()
        print("BANKING SYSTEM MANAGEMENT")
        line()
        print("1. Create New Account")
        print("2. Login to Existing Account")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            create_account_ui(bank)
        elif choice == "2":
            login_ui(bank)
        elif choice == "3":
            print("Thank you for using our Banking System. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
