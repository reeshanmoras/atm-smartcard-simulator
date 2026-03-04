# atm_app/admin.py

import os
import calendar

from atm_app.customer import load_accounts, save_accounts
from atm_app.account import Account
from atm_app.utils import (
    TXN_FILE,
    load_json,
    clear_screen,
    pause,
)

# Optional imports for Lab: NumPy & Pandas
try:
    import numpy as np
    import pandas as pd
except ImportError:
    np = None
    pd = None


def create_account():
    accounts = load_accounts()
    acc_no = input("Enter new account number: ")

    if acc_no in accounts:
        print("Account number already exists.")
        return

    name = input("Enter customer name: ")
    pin = input("Set 4-digit PIN: ")
    try:
        opening = float(input("Enter opening balance: "))
    except ValueError:
        opening = 0.0

    acc = Account(acc_no, name, pin, opening)
    accounts[acc_no] = acc
    save_accounts(accounts)
    print("Account created successfully.")


def list_accounts():
    accounts = load_accounts()
    if not accounts:
        print("No accounts found.")
        return

    print("Acc No   Name                Balance")
    print("--------------------------------------")
    for acc in accounts.values():
        print(f"{acc.acc_no:<8} {acc.name:<18} {acc.balance:>8.2f}")


def show_transactions_basic():
    txns = load_json(TXN_FILE, [])
    if not txns:
        print("No transactions yet.")
        return
    for t in txns[-10:]:  # last 10
        print(
            f"{t['timestamp']} | Acc:{t['acc_no']} | {t['type']} | Amount:{t['amount']}"
        )


def show_transactions_stats_numpy():
    if np is None:
        print("NumPy not installed. Please install numpy to see statistics.")
        return

    txns = load_json(TXN_FILE, [])
    if not txns:
        print("No transactions to analyse.")
        return

    amounts = np.array([float(t["amount"]) for t in txns])
    print("===== NumPy Transaction Stats =====")
    print("Total:", amounts.sum())
    print("Average:", amounts.mean())
    print("Max:", amounts.max())
    print("Min:", amounts.min())


def show_transactions_with_pandas():
    if pd is None:
        print("Pandas not installed. Please install pandas to use this feature.")
        return

    if not os.path.exists(TXN_FILE):
        print("Transaction file not found.")
        return

    # read JSON as DataFrame
    txns = load_json(TXN_FILE, [])
    if not txns:
        print("No transactions.")
        return

    df = pd.DataFrame(txns)
    print("First 5 rows:")
    print(df.head())
    print("\nLast 5 rows:")
    print(df.tail())


def file_permission_info():
    """
    Demo of os.access() and simple permission check (Lab 5: OS Module).
    """
    path = TXN_FILE
    print(f"Checking permissions for: {path}")
    print("Readable:", os.access(path, os.R_OK))
    print("Writable:", os.access(path, os.W_OK))
    print("Executable:", os.access(path, os.X_OK))


def show_calendar_menu():
    """
    Demo of calendar.month and calendar.calendar.
    """
    try:
        year = int(input("Enter year (e.g., 2025): "))
    except ValueError:
        print("Invalid year.")
        return

    try:
        month = int(input("Enter month (1-12): "))
    except ValueError:
        print("Invalid month.")
        return

    if 1 <= month <= 12:
        print("\nCalendar for specified month:")
        print(calendar.month(year, month))
    else:
        print("Invalid month.")

    print("\nFull year calendar:")
    print(calendar.calendar(year))


def admin_menu():
    while True:
        clear_screen()
        print("===== ADMIN MENU =====")
        print("1. Create account")
        print("2. List all accounts")
        print("3. View last 10 transactions")
        print("4. Additional Features")
        print("5. Back to main menu")

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
            pause()
        elif choice == "2":
            list_accounts()
            pause()
        elif choice == "3":
            show_transactions_basic()
            pause()
        elif choice == "4":
            additional_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
            pause()
def additional_menu():
    while True:
        clear_screen()
        print("===== ADDITIONAL FEATURES =====")
        print("1. View transaction statistics (NumPy)")
        print("2. View transactions as table (Pandas)")
        print("3. Check data file permissions (os.access)")
        print("4. Calendar view (calendar module)")
        print("5. Back to admin menu")

        choice = input("Enter choice: ")

        if choice == "1":
            show_transactions_stats_numpy()
            pause()
        elif choice == "2":
            show_transactions_with_pandas()
            pause()
        elif choice == "3":
            file_permission_info()
            pause()
        elif choice == "4":
            show_calendar_menu()
            pause()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
            pause()

