def line():
    print("-" * 55)


def create_account_ui(bank):
    line()
    print("CREATE NEW ACCOUNT")
    line()
    name = input("Enter your name: ").strip()

    while True:
        pin = input("Set a 4-digit PIN: ").strip()
        if pin.isdigit() and len(pin) == 4:
            break
        print("PIN must be exactly 4 digits!")

    while True:
        try:
            deposit = float(input("Initial deposit amount (min 500): "))
            if deposit >= 500:
                break
            print("Minimum initial deposit is 500.")
        except ValueError:
            print("Enter a valid number.")

    acc_no = bank.create_account(name, pin, deposit)
    line()
    print("Account created successfully!")
    print(f"Your Account Number is: {acc_no}")
    print("Please save this number, you will need it to login.")
    line()


def login_ui(bank):
    line()
    print("LOGIN")
    line()
    acc_no = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    if bank.authenticate(acc_no, pin):
        print(f"\nWelcome, {bank.accounts[acc_no]['name']}!")
        account_menu(bank, acc_no)
    else:
        print("Invalid Account Number or PIN!")


def account_menu(bank, acc_no):
    while True:
        line()
        print(f"ACCOUNT MENU | Acc No: {acc_no}")
        line()
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Update Account Details")
        print("7. Close Account")
        print("8. Logout")

        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            amt = float(input("Enter amount to deposit: "))
            bank.deposit(acc_no, amt)
            print(f"Deposited {amt}. New Balance: {bank.check_balance(acc_no)}")

        elif choice == "2":
            amt = float(input("Enter amount to withdraw: "))
            success, msg = bank.withdraw(acc_no, amt)
            print(msg)

        elif choice == "3":
            print(f"Current Balance: {bank.check_balance(acc_no)}")

        elif choice == "4":
            to_acc = input("Enter receiver's Account Number: ").strip()
            amt = float(input("Enter amount to transfer: "))
            success, msg = bank.transfer(acc_no, to_acc, amt)
            print(msg)

        elif choice == "5":
            txns = bank.get_transactions(acc_no)
            line()
            print("TRANSACTION HISTORY")
            line()
            if not txns:
                print("No transactions yet.")
            for t in txns:
                print(f"{t['date']} | {t['type']:<25} | Amount: {t['amount']}")

        elif choice == "6":
            new_name = input("Enter new name (leave blank to skip): ").strip()
            new_pin = input("Enter new 4-digit PIN (leave blank to skip): ").strip()
            bank.update_details(
                acc_no,
                new_name if new_name else None,
                new_pin if new_pin else None,
            )
            print("Details updated successfully!")

        elif choice == "7":
            confirm = input("Are you sure you want to close account? (yes/no): ")
            if confirm.lower() == "yes":
                bank.close_account(acc_no)
                print("Account closed successfully.")
                break

        elif choice == "8":
            print("Logged out.")
            break

        else:
            print("Invalid choice, try again.")
