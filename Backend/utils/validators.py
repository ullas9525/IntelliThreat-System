
import re

def validate_register_input(data):
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return False, "Missing required fields"
    
    if len(data['password']) < 6:
        return False, "Password must be at least 6 characters"
    
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, data['email']):
        return False, "Invalid email format"
        
    return True, "Valid"

def validate_log_input(data):
    required = ['user_id', 'session_duration', 'data_download_mb', 'transaction_amount', 'access_count', 'login_frequency', 'failed_logins', 'role']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, "Valid"
