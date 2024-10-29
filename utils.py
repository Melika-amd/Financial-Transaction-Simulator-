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