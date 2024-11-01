import random

# List of first names and last names for random generation
first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph",
    "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Emma", "Noah", "Olivia",
    "Liam", "Ava", "Sophia", "Mason", "Isabella", "Lucas", "Mia"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
    "Harris", "Clark", "Lewis", "Robinson", "Walker", "Hall", "Young"
]

def generate_random_name():
    """Generate a random full name"""
    first = random.choice(first_names)
    last = random.choice(last_names)
    return f"{first} {last}"

def calculate_risk_score(amount, transaction_type):
    """
    Calculate risk score based on amount and transaction type
    Returns a score between 0 and 1
    """
    # Base risk on amount
    amount_risk = min(amount / 10000, 1)  # Higher amounts = higher risk, max at 10000
    
    # Risk weights for different transaction types
    type_risk = {
        "PAYMENT": 0.2,
        "TRANSFER": 0.3,
        "DEBIT": 0.4,
        "CASH_OUT": 0.5
    }
    
    # Calculate final risk score
    risk_score = (amount_risk * 0.7) + (type_risk.get(transaction_type, 0.3) * 0.3)
    return round(risk_score, 2) 