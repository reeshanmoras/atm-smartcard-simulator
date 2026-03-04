# atm_app/utils.py

import os
import json
from datetime import datetime, timedelta
from functools import reduce
from atm_app.account import Account  


DATA_DIR = "data"
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TXN_FILE = os.path.join(DATA_DIR, "transactions.json")


# DIRECTORY CHECK
def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


# JSON LOAD / SAVE
def load_json(path, default):
    ensure_data_dir()
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default


def save_json(path, data):
    ensure_data_dir()
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ACCOUNT LOAD / SAVE
def load_accounts() -> dict:
    """
    Loads all accounts as a dictionary of acc_no -> Account objects
    """
    raw = load_json(ACCOUNTS_FILE, {})
    accounts = {}
    for acc_no, data in raw.items():
        accounts[acc_no] = Account.from_dict(data)
    return accounts


def save_accounts(accounts: dict):
    """
    Saves dictionary of Account objects into accounts.json
    """
    raw = {acc_no: acc.to_dict() for acc_no, acc in accounts.items()}
    save_json(ACCOUNTS_FILE, raw)


# TRANSACTION LOGGING
def log_transaction(acc_no, amount, tx_type):
    """
    Logs a single transaction entry.
    """
    transactions = load_json(TXN_FILE, [])
    entry = {
        "acc_no": acc_no,
        "amount": amount,
        "type": tx_type,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    transactions.append(entry)
    save_json(TXN_FILE, transactions)


# SCREEN + PAUSE HELPERS
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("Press Enter to continue...")


# TOTAL TRANSACTION AMOUNT
def total_amount_for_account(acc_no: str) -> float:
    txns = load_json(TXN_FILE, [])
    amounts = [tx["amount"] for tx in txns if tx["acc_no"] == acc_no]
    return reduce(lambda x, y: x + y, amounts, 0.0)


def next_due_date(days: int = 30) -> datetime:
    return datetime.now() + timedelta(days=days)
