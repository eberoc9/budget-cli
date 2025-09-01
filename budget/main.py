import argparse
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
EXPENSES_FILE = Path("expenses.json")

"""
JSON helpers
"""
def ensure_storage():
    """
    Ensure that data directory and file exist. Create one if it doesn't
    """
    DATA_DIR.mkdir(exist_ok=True)
    if not Path(DATA_DIR/EXPENSES_FILE).exists():
        Path(DATA_DIR/EXPENSES_FILE).write_text("[]", encoding="utf-8")

def load_expenses():
    """
    Load expenses from JSON file.
    Return empty list if file is missing.
    """
    ensure_storage()
    
    try:    
        with Path(DATA_DIR/EXPENSES_FILE).open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        save_expenses([]) # reset corrupted file
        return []
    
def save_expenses(expenses):
    """
    Save expenses list to JSON file.
    """
    ensure_storage()
    with Path(DATA_DIR/EXPENSES_FILE).open("w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)

"""
Command implementations
"""
def add_expense(args) -> None:
    """
    Add an new expense record to storage.
    """
    expenses = load_expenses()
    new_id = (
        max(
            [e["id"] for e in expenses]
        ) + 1
    ) if expenses else 1

    expense = {
        "id": new_id,
        "amount": args.amount,
        "category": args.category,
        "note": args.note or "",
        "date": datetime.now().isoformat(timespec="seconds")
    }

    expenses.append(expense)
    save_expenses(expenses)

    print(f"Added expense #{new_id}: {args.amount} in {args.category} - {args.note}")

def list_expenses(args):
    """
    List all stored expenses
    """
    expenses = load_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return
    
    for expense in expenses:
        print(
            f"#{expense['id']} | {expense['date']} | {expense['category']} | Php{expense['amount']:.2f} | {expense['note']}"
        )
    print("Listing all expenses (Under development)")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="budget",
        description="CLI tool for budgeting and monitoring spending"
    )

    subparsers = parser.add_subparsers(dest="command")

    # add commands
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Add a new expense")
    add_parser.add_argument("category", help="Expense category (e.g. food, transportation, etc.)")
    add_parser.add_argument("-n", "--note", help="Optional note", default="")
    add_parser.set_defaults(func=add_expense)

    # list commands
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.set_defaults(func=list_expenses)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Check if args have a function
    """
    Sample: python budget/main.py
    Result: Show help
    """
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()