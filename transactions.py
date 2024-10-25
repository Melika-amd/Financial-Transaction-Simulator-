import random
import pandas as pd
from datetime import datetime, timedelta

def generate_users(num_users=10):
    users = []
    for i in range(1, num_users + 1):
        user = {
            "UserID": f"User_{i}",
            "Location": random.choice(["NY", "LA", "Toronto", "Vancouver", "Chicago"]),
            "SpendingBehavior": random.choice(["Low", "Moderate", "High"]),
            "TransactionFrequency": random.randint(1, 10)
        }
        users.append(user)
    return users

def generate_transaction_type():
    types = [
        "Bank Transfer", 
        "POS Payment", 
        "ATM Withdrawal", 
        "Refund", 
        "Chargeback", 
        "Cross-Border Payment"
    ]
    return random.choice(types)

def generate_transaction_amount(transaction_type):
    amount = random.uniform(10, 5000)
    if transaction_type in ["Refund", "Chargeback"]:
        return round(-amount, 2)
    elif transaction_type == "ATM Withdrawal":
        return round(min(amount, 500), 2)
    elif transaction_type == "Cross-Border Payment":
        return round(amount * 1.3, 2)
    else:
        return round(amount, 2)

def generate_transaction_timestamp():
    now = datetime.now()
    random_day = now - timedelta(days=random.randint(0, 30))
    if random.random() < 0.3:
        random_day += timedelta(days=(5 - random_day.weekday()) % 7)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    return datetime(random_day.year, random_day.month, random_day.day, random_hour, random_minute)

def is_fraudulent(sender, amount, timestamp, failed_attempts=0):
    if amount > 4000:
        return True
    if timestamp.hour < 6:
        return True
    if failed_attempts >= 3:
        return True
    if sender["SpendingBehavior"] == "Low" and amount > 1000:
        return True
    return False

def assign_risk_score(transaction):
    score = 0
    if transaction["IsFraud"]:
        score += 2
    if transaction["Amount"] > 2000:
        score += 1
    return min(score, 3)

def generate_transactions(users, num_transactions=100):
    transactions = []
    for _ in range(num_transactions):
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u != sender])
        t_type = generate_transaction_type()
        amount = generate_transaction_amount(t_type)
        timestamp = generate_transaction_timestamp()
        is_fraud = is_fraudulent(sender, amount, timestamp)
        transactions.append({
            "Sender": sender["UserID"],
            "Receiver": receiver["UserID"],
            "Type": t_type,
            "Amount": amount,
            "Timestamp": timestamp,
            "IsFraud": is_fraud
        })
    return pd.DataFrame(transactions)

def generate_transactions_with_risk(users, num_transactions=100):
    transactions = generate_transactions(users, num_transactions)
    transactions["RiskScore"] = transactions.apply(assign_risk_score, axis=1)
    return transactions

users = generate_users(5)
transactions = generate_transactions_with_risk(users, 20)
print(transactions)
