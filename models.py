from dataclasses import dataclass, asdict
import uuid
from datetime import date


@dataclass
class User:
    user_id: str
    name: str
    password: str      
    currency: str = "USD"

    @staticmethod
    def create(name: str, password_hash: str, currency: str = "USD") -> "User":
        return User(
            user_id=str(uuid.uuid4()),
            name=name,
            password=password_hash,
            currency=currency.upper() if currency else "USD",
        )
    @staticmethod
    def from_dict(d: dict) -> "User":
        return User(**d)
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Transaction:
    transaction_id: str
    user_id: str
    type: str           # "income" or "expense"
    amount: float
    category: str
    date: str
    description: str
    payment_method: str

    @staticmethod
    def create(
        user_id: str,
        type: str,
        amount: float,
        category: str,
        description: str,
        payment_method: str,
    ) -> "Transaction":
        return Transaction(
            transaction_id=f"TXN-{uuid.uuid4().hex[:6].upper()}",
            user_id=user_id,
            type=type.lower(),
            amount=round(float(amount), 2),
            category=category.title(),
            date=str(date.today()),
            description=description,
            payment_method=payment_method.title(),
        )
    def to_dict(self) -> dict:
        return asdict(self)   
    @staticmethod
    def from_dict(d: dict) -> "Transaction":
        # CSV loader returns strings; fix numeric fields here if needed.
        d = d.copy()
        d["amount"] = float(d["amount"])
        # keep date as-is (already a string like "YYYY-MM-DD")
        return Transaction(**d)   