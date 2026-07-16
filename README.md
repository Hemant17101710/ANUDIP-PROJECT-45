import json
import os
import random
from datetime import datetime

DATA_FILE = "bank_data.json"


# ----------------------------------------------------------
# Data handling functions (JSON file = simple database)
# ----------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ----------------------------------------------------------
# Bank class - core logic
# ----------------------------------------------------------
class Bank:
    def __init__(self):
        self.accounts = load_data()

    # ---------- helper ----------
    def generate_account_number(self):
        while True:
            acc_no = str(random.randint(100000, 999999))
            if acc_no not in self.accounts:
                return acc_no

    def add_transaction(self, acc_no, txn_type, amount):
        txn = {
            "type": txn_type,
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
        self.accounts[acc_no]["transactions"].append(txn)

    # ---------- core features ----------
    def create_account(self, name, pin, initial_deposit):
        acc_no = self.generate_account_number()
        self.accounts[acc_no] = {
            "name": name,
            "pin": pin,
            "balance": initial_deposit,
            "transactions": [],
        }
        self.add_transaction(acc_no, "Account Opened / Initial Deposit", initial_deposit)
        save_data(self.accounts)
        return acc_no

    def authenticate(self, acc_no, pin):
        account = self.accounts.get(acc_no)
        if account and account["pin"] == pin:
            return True
        return False

    def deposit(self, acc_no, amount):
        self.accounts[acc_no]["balance"] += amount
        self.add_transaction(acc_no, "Deposit", amount)
        save_data(self.accounts)

    def withdraw(self, acc_no, amount):
        if amount > self.accounts[acc_no]["balance"]:
            return False, "Insufficient balance!"
        self.accounts[acc_no]["balance"] -= amount
        self.add_transaction(acc_no, "Withdraw", amount)
        save_data(self.accounts)
        return True, "Withdraw successful!"

    def check_balance(self, acc_no):
        return self.accounts[acc_no]["balance"]

    def transfer(self, from_acc, to_acc, amount):
        if to_acc not in self.accounts:
            return False, "Receiver account does not exist!"
        if amount > self.accounts[from_acc]["balance"]:
            return False, "Insufficient balance!"
        self.accounts[from_acc]["balance"] -= amount
        self.accounts[to_acc]["balance"] += amount
        self.add_transaction(from_acc, f"Transfer to {to_acc}", amount)
        self.add_transaction(to_acc, f"Transfer from {from_acc}", amount)
        save_data(self.accounts)
        return True, "Transfer successful!"

    def update_details(self, acc_no, new_name=None, new_pin=None):
        if new_name:
            self.accounts[acc_no]["name"] = new_name
        if new_pin:
            self.accounts[acc_no]["pin"] = new_pin
        save_data(self.accounts)

    def close_account(self, acc_no):
        del self.accounts[acc_no]
        save_data(self.accounts)

    def get_transactions(self, acc_no):
        return self.accounts[acc_no]["transactions"]


# ----------------------------------------------------------
# Console interface (Menu Driven)
# ----------------------------------------------------------
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
        print(f"ACCOUNT MENU  |  Acc No: {acc_no}")
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
