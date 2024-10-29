import random
import pandas as pd
from datetime import datetime, timedelta
from utils import generate_random_name

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

def is_fraudulent(amount, timestamp, failed_attempts=0):
    if amount > 4000:
        return True
    if timestamp.hour < 6:
        return True
    if failed_attempts >= 3:
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
        sender = generate_random_name()
        receiver = generate_random_name()
        while receiver == sender:
            receiver = generate_random_name()
        t_type = generate_transaction_type()
        amount = generate_transaction_amount(t_type)
        timestamp = generate_transaction_timestamp()
        is_fraud = is_fraudulent(amount, timestamp)
        transactions.append({
            "Sender": sender,
            "Receiver": receiver,
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

def export_transactions_to_csv(transactions_df, filename="transactions_export.csv"):
    """
    Export transactions DataFrame to a CSV file
    
    Args:
        transactions_df (pd.DataFrame): DataFrame containing transactions
        filename (str): Name of the output CSV file
    
    Returns:
        str: Path to the exported CSV file
    """
    try:
        transactions_df.to_csv(filename, index=False)
        return filename
    except Exception as e:
        print(f"Error exporting transactions: {str(e)}")
        return None

users = generate_users(5)
transactions = generate_transactions_with_risk(users, 20)
print(transactions)
