import random
from datetime import datetime

from data_handler import load_data, save_data


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
