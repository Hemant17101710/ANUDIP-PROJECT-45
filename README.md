# Banking System Management

A simple console-based banking system built in Python, using a JSON file as a lightweight local database.

## Features
- Create a new account (name, PIN, initial deposit)
- Login with account number and PIN
- Deposit / Withdraw money
- Transfer money between accounts
- View transaction history
- Update account details (name/PIN)
- Close account

## Project Structure
```
banking_system/
├── main.py           # Entry point - runs the console app
├── bank.py           # Bank class - core account logic
├── data_handler.py   # JSON file read/write (storage layer)
├── ui.py             # Console menus and user interaction
└── README.md
```

## Usage
```bash
python main.py
```

Account data is stored in `bank_data.json`, created automatically in the same directory on first run.

