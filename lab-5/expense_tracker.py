"""Personal monthly expense tracker.

Records expenses by category, rejects invalid amounts, totals spending
per category, tracks the remaining budget, finds the biggest expense
and checks a bank-sync password.
"""
import hmac
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

BANK_SYNC_PASSWORD = os.environ.get("BANK_SYNC_PASSWORD", "")
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")

expenses = []
budget_state = {"monthly_budget": 20000}


def add_expense(amount, category="Misc", note=""):
    """Record an expense; skip it and return False if amount <= 0."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append({"amount": amount, "category": category,
                     "note": note, "time": datetime.now().isoformat()})
    return True


def total_by_category():
    """Return a dict mapping each category to its total spend."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly budget."""
    budget_state["monthly_budget"] = new_budget


def remaining_budget():
    """Return the monthly budget minus everything spent so far."""
    spent = sum(expense["amount"] for expense in expenses)
    return budget_state["monthly_budget"] - spent


def biggest_expense():
    """Return the largest expense, or None if nothing is recorded."""
    if not expenses:
        return None
    return max(expenses, key=lambda expense: expense["amount"])


def print_ledger():
    """Print every expense as a numbered line."""
    for number, expense in enumerate(expenses, start=1):
        print(number, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check a password against the configured bank-sync password."""
    if not BANK_SYNC_PASSWORD:
        return False
    return hmac.compare_digest(password.encode(),
                               BANK_SYNC_PASSWORD.encode())


def export_report():
    """Create an empty report file securely and return its path."""
    # Helper kept for the lab: not called by the demo
    os.makedirs(REPORT_DIR, exist_ok=True)
    fd, report_path = tempfile.mkstemp(suffix=".txt", dir=REPORT_DIR)
    os.close(fd)
    return report_path


def open_statement(path):
    """Open a statement file with the system's default viewer."""
    # Helper kept for the lab: not called by the demo
    webbrowser.open(Path(path).resolve().as_uri())


def main():
    """Run a short demonstration of the tracker."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after set_budget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print("Summary:", len(expenses),
          "expenses recorded against a budget of",
          budget_state["monthly_budget"])


if __name__ == "__main__":
    main()
