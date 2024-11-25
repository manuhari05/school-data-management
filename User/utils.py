import string
import random


from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



def generate_random_password(length=8):
    """Generate a random password that includes letters, digits, and special characters."""
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")
    
    # Ensure the password contains at least one of each required character type
    characters = string.ascii_letters + string.digits + '!@#$%^&*(),.?":{}|<>'
    
    password = [
        random.choice(string.ascii_uppercase),  # At least one uppercase letter
        random.choice(string.ascii_lowercase),  # At least one lowercase letter
        random.choice(string.digits),            # At least one digit
        random.choice('!@#$%^&*(),.?:{}|<>')   # At least one special character
    ]

    # Fill the rest of the password length with random choices from all characters
    password += random.choices(characters, k=length - len(password))
    
    # Shuffle the result to avoid predictable sequences
    random.shuffle(password)

    return ''.join(password)