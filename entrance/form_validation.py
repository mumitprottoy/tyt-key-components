import re
from django.contrib.auth.models import User
from utils.operations import passes_check_list
from utils.constants import REGEX as reg


def validate_creds_from_signup_form(
        first_name: str, last_name: str, username: str, email: str, password: str, confirm_password: str) -> tuple[bool, str]:
    
    check_list = [
        (bool(re.match(reg['name'], first_name)), 'First name can only contain letters.', 'first_name'),
        
        (bool(re.match(reg['name'], last_name)), 'Last name can only contain letters.', 'last_name'),
        
        ( not User.objects.filter(username=username).exists(), "Username already exists.", "username" ),
        
        ( "@" in email and len(email.split('@')) == 2, "Email syntax is invalid.", "email" ),
        
        ( bool(re.match(reg['username'], username)), "Invalid username.", "username" ),
        
        ( not User.objects.filter(email=email).exists(), "Email already exists.", "email" ),
        
        ( len(password) >= 8, "Password must have at least 8 characters.", "password" ),
        
        ( password == confirm_password, "Passwords did not match.", "confirm_password" )
    ]  

    return passes_check_list(check_list=check_list, check_all=True)
    