import re

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return "Username must be between 3 and 20 characters"
    
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return "Username can only contain letters, numbers, and underscores"
    
    return None


def validate_password(password):
    if len(password) < 6:
        return "Password must be at least 6 characters"
    
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one number"
    
    return None