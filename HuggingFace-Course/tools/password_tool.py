from smolagents import tool
import random
import string

@tool
def generate_password(length: int = 12, include_special: bool = True) -> str:
    """Generate a secure random password
    Args:
        length: Length of password (default: 12)
        include_special: Include special characters (default: True)
    """
    try:
        if length < 8:
            return "Password length must be at least 8 characters"
        
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation
            
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Ensure password contains at least one of each required type
        if not any(c.isupper() for c in password):
            password = random.choice(string.ascii_uppercase) + password[1:]
        if not any(c.islower() for c in password):
            password = password[:-1] + random.choice(string.ascii_lowercase)
        if not any(c.isdigit() for c in password):
            pos = random.randint(1, len(password)-2)
            password = password[:pos] + random.choice(string.digits) + password[pos+1:]
            
        return f"Generated password: {password}"
    except Exception as e:
        return f"Error generating password: {str(e)}" 