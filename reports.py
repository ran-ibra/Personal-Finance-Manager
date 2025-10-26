import json
import os
from datetime import datetime
from typing import Dict
from transactions import TransactionManager


BUDGET_FILE = "budgets.json"


class ReportsManager:
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager
        self.budgets = self._load_budgets()


    def _load_budgets(self) -> Dict[str, Dict]:
        if os.path.exists(BUDGET_FILE):
            try:
                with open(BUDGET_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_budgets(self):
    
        with open(BUDGET_FILE, "w") as f:
            json.dump(self.budgets, f, indent=4)

    def set_monthly_budget(self, username: str, month: str, limit: float):
        
        if username not in self.budgets:
            self.budgets[username] = {}
        self.budgets[username][month] = {"limit": limit}
        self._save_budgets()
        print(f" Budget for {month} set to ${limit:,.2f}")

    def budget_status(self, username: str, month: str) -> Dict[str, float]:
        budget = self.budgets.get(username, {}).get(month)
        if not budget:
            return {"message": f"No budget set for {month}. Please set one first."}

        transactions = self.transaction_manager.get_user_transactions(username)
        expenses = sum(
            t["amount"] for t in transactions
            if t["type"] == "expense" and t["date"].startswith(month)
        )

        limit = budget["limit"]
        remaining = limit - expenses
        percent_used = min(100, round((expenses / limit) * 100, 2)) if limit > 0 else 0

        status = {
            "Month": month,
            "Budget Limit": f"${limit:,.2f}",
            "Expenses": f"${expenses:,.2f}",
            "Remaining": f"${remaining:,.2f}",
            "Used (%)": f"{percent_used}%",
        }

        if expenses > limit:
            status["Warning"] = "You have exceeded your monthly budget!"
        elif percent_used >= 90:
            status["Caution"] = "You are close to exceeding your budget."
        else:
            status["Status"] = "You are within your budget."

        return status

    def calculate_health_score(self, username: str) -> Dict[str, float]:
       
        txns = self.transaction_manager.get_user_transactions(username)
        if not txns:
            return {"score": 0, "message": "No transactions available yet."}

        income = sum(t["amount"] for t in txns if t["type"] == "income")
        expenses = sum(t["amount"] for t in txns if t["type"] == "expense")
        if income == 0:
            return {"score": 30, "message": "No income recorded — please add income transactions."}

        savings_ratio = max(0, (income - expenses) / income)  # higher = better
        expense_count = sum(1 for t in txns if t["type"] == "expense")
        avg_expense = expenses / expense_count if expense_count > 0 else 0

        score = (
            (savings_ratio * 60)  
            + (min(1, 5000 / (avg_expense + 1)) * 20)  
            + (min(1, 20 / (expense_count + 1)) * 20) 
        )

        # Normalize score to 100
        score = min(100, round(score, 2))

        # Feedback
        if score >= 80:
            note = "💚 Excellent financial health! Keep it up."
        elif score >= 60:
            note = "💛 Good balance. Review your spending habits for improvement."
        elif score >= 40:
            note = "🟠 Caution: Expenses are high compared to income."
        else:
            note = "🔴 Poor health. Reduce expenses or increase savings."

        return {"score": score, "message": note}

    # -----------------------------
    # Existing Reports
    # -----------------------------
    def dashboard_summary(self, username: str) -> Dict[str, float]:
        txns = self.transaction_manager.get_user_transactions(username)
        income = sum(t["amount"] for t in txns if t["type"] == "income")
        expenses = sum(t["amount"] for t in txns if t["type"] == "expense")
        return {
            "Total Income": f"${income:,.2f}",
            "Total Expenses": f"${expenses:,.2f}",
            "Net Balance": f"${(income - expenses):,.2f}"
        }

    def category_breakdown(self, username: str) -> Dict[str, float]:
        txns = self.transaction_manager.get_user_transactions(username)
        summary = {}
        for t in txns:
            if t["type"] == "expense":
                summary[t["category"]] = summary.get(t["category"], 0) + t["amount"]
        return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

    def monthly_report(self, username: str, month: str) -> Dict[str, float]:
        txns = self.transaction_manager.get_user_transactions(username)
        month_txns = [t for t in txns if t["date"].startswith(month)]
        income = sum(t["amount"] for t in month_txns if t["type"] == "income")
        expense = sum(t["amount"] for t in month_txns if t["type"] == "expense")
        return {
            "Month": month,
            "Income": f"${income:,.2f}",
            "Expense": f"${expense:,.2f}",
            "Balance": f"${(income - expense):,.2f}",
            "Transaction Count": len(month_txns)
        }

  
    def print_report(self, title: str, data: Dict):
        print("\n" + "=" * 60)
        print(title.center(60))
        print("=" * 60)
        for key, value in data.items():
            print(f"{key:<25}: {value}")
        print("=" * 60)