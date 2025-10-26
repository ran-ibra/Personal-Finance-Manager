import json
import os
from datetime import datetime, timedelta
from transactions import TransactionManager

GOALS_FILE = "savings_goals.json"
RECURRING_FILE = "recurring_transactions.json"


class AdvancedFeatures:
    def __init__(self, transaction_manager: TransactionManager):
        self.transaction_manager = transaction_manager
        self.goals = self._load_json(GOALS_FILE)
        self.recurring = self._load_json(RECURRING_FILE)

    # -----------------------------
    # Shared JSON Helpers
    # -----------------------------
    def _load_json(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_json(self, filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def set_savings_goal(self, username: str, goal_name: str, target_amount: float):
        """Create or update a savings goal."""
        if username not in self.goals:
            self.goals[username] = {}
        self.goals[username][goal_name] = {
            "target": target_amount,
            "saved": 0.0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._save_json(GOALS_FILE, self.goals)
        print(f"Goal '{goal_name}' created with target ${target_amount:,.2f}")

    def update_savings_progress(self, username: str):
        """Recalculate savings progress based on user's income transactions."""
        if username not in self.goals:
            return None

        user_txns = self.transaction_manager.get_user_transactions(username)
        total_income = sum(t["amount"] for t in user_txns if t["type"] == "income")
        total_expense = sum(t["amount"] for t in user_txns if t["type"] == "expense")
        net_savings = max(total_income - total_expense, 0)

        for goal_name, goal in self.goals[username].items():
            goal["saved"] = min(goal["target"], net_savings)

        self._save_json(GOALS_FILE, self.goals)

    def get_savings_goals(self, username: str):
        """Get all savings goals with progress percentage."""
        self.update_savings_progress(username)
        if username not in self.goals or not self.goals[username]:
            return {"message": "No savings goals found."}

        result = {}
        for name, goal in self.goals[username].items():
            progress = (goal["saved"] / goal["target"]) * 100 if goal["target"] > 0 else 0
            result[name] = {
                "Target": f"${goal['target']:,.2f}",
                "Saved": f"${goal['saved']:,.2f}",
                "Progress (%)": f"{progress:.1f}%",
            }
        return result

    # ============================================================
    def add_recurring_transaction(
        self, username: str, amount: float, category: str,
        description: str, t_type: str, frequency: str
    ):
        
        if username not in self.recurring:
            self.recurring[username] = []

        next_date = datetime.now().strftime("%Y-%m-%d")
        entry = {
            "amount": amount,
            "category": category,
            "description": description,
            "type": t_type,
            "frequency": frequency.lower(),
            "next_date": next_date,
        }
        self.recurring[username].append(entry)
        self._save_json(RECURRING_FILE, self.recurring)
        print(f"Recurring {t_type} of ${amount:.2f} added ({frequency.capitalize()})")

    def process_recurring_transactions(self, username: str):
        """Check if any recurring transactions are due and apply them."""
        if username not in self.recurring:
            return

        today = datetime.now().date()
        updated = False

        for r in self.recurring[username]:
            next_date = datetime.strptime(r["next_date"], "%Y-%m-%d").date()
            if today >= next_date:
                # Add transaction
                self.transaction_manager.add_transaction(
                    username,
                    r["amount"],
                    r["category"],
                    r["description"],
                    r["type"]
                )
                print(f"Processed {r['frequency']} {r['type']} of ${r['amount']:.2f}")

                # Schedule next recurrence
                if r["frequency"] == "daily":
                    next_date += timedelta(days=1)
                elif r["frequency"] == "weekly":
                    next_date += timedelta(weeks=1)
                elif r["frequency"] == "monthly":
                    next_date += timedelta(days=30)

                r["next_date"] = next_date.strftime("%Y-%m-%d")
                updated = True

        if updated:
            self._save_json(RECURRING_FILE, self.recurring)

    def get_recurring_transactions(self, username: str):
        return self.recurring.get(username, [])
