from datetime import datetime
from typing import Dict, List
from transactions import TransactionManager


class ReportsManager:
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager

    def dashboard_summary(self, username: str) -> Dict[str, float]:
        """Calculate total income, expenses, and balance for the user."""
        user_txns = self.transaction_manager.get_user_transactions(username)
        total_income = sum(t.get("amount", 0) for t in user_txns if t.get("type") == "income")
        total_expense = sum(t.get("amount", 0) for t in user_txns if t.get("type") == "expense")
        balance = total_income - total_expense

        return {
            "Total Income": round(total_income, 2),
            "Total Expense": round(total_expense, 2),
            "Net Balance": round(balance, 2)
        }


    def monthly_report(self, username: str, month: str) -> Dict[str, float]:
        """Summarize income, expenses, and count for a specific month (YYYY-MM)."""
        user_txns = self.transaction_manager.get_user_transactions(username)

        def in_month(txn):
            try:
                return txn["date"].startswith(month)
            except (KeyError, AttributeError):
                return False

        monthly_txns = [t for t in user_txns if in_month(t)]

        income = sum(t["amount"] for t in monthly_txns if t["type"] == "income")
        expense = sum(t["amount"] for t in monthly_txns if t["type"] == "expense")

        return {
            "Month": month,
            "Income": round(income, 2),
            "Expense": round(expense, 2),
            "Net Balance": round(income - expense, 2),
            "Transaction Count": len(monthly_txns)
        }


    def category_breakdown(self, username: str) -> Dict[str, float]:
        """Show spending by category (expenses only)."""
        user_txns = self.transaction_manager.get_user_transactions(username)
        category_totals: Dict[str, float] = {}

        for t in user_txns:
            if t["type"] == "expense":
                cat = t.get("category", "Uncategorized")
                category_totals[cat] = category_totals.get(cat, 0) + t.get("amount", 0)

        # Sort by descending spending
        return dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))


    @staticmethod
    def _print_header(title: str):
        print("\n" + "=" * 60)
        print(title.center(60))
        print("=" * 60)

    @staticmethod
    def _print_footer():
        print("=" * 60)

    def print_report(self, title: str, data: Dict[str, float]):
        """Nicely formatted report display."""
        self._print_header(title)

        if not data:
            print(" No data available for this report.")
            self._print_footer()
            return

        # Detect if it's a category breakdown (dict of many keys)
        if all(isinstance(v, (int, float)) for v in data.values()) and len(data) > 5:
            self._print_category_table(data)
        else:
            for key, value in data.items():
                formatted = f"${value:,.2f}" if isinstance(value, (int, float)) else str(value)
                print(f"{key:<25}: {formatted}")
        self._print_footer()

    def _print_category_table(self, data: Dict[str, float]):
        """Render category breakdown as a mini chart."""
        total = sum(data.values()) or 1  # Avoid division by zero
        print(f"{'Category':<20} | {'Amount':>10} | {'Chart'}")
        print("-" * 60)

        for category, amount in data.items():
            bar_length = int((amount / total) * 30)
            bar = "█" * bar_length
            print(f"{category:<20} | ${amount:>9.2f} | {bar}")
