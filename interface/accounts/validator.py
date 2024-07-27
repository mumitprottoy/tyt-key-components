import re
from django.contrib.auth.models import User
from accounts.models import ContactInfo
from utils.constants import REGEX


class UserInfoValidator:

    def filter_name(first_name: str, last_name: str) -> list[str]:
        names: list[str] = [first_name, last_name]
        for n in range(len(names)):
            if len(names[n]) > 0:
                chars = list(names[n])
                if chars[0].isalpha():
                    chars[0] = chars[0].upper()

                for i in range(1, len(chars)):
                    if chars[i-1] == '.' or chars[i-1] == ' ':
                        if chars[i].isalpha():
                            chars[i] = chars[i].upper()

                names[n] = ''.join(chars)
                names[n] = re.sub(REGEX['name_sub'], '', names[n])

        return names
    
    
    def validate_not_empty(data) -> bool:
        return len(str(data)) > 0
    

    def validate_username(username: str) -> bool:
        return not User.objects.filter(username=username).exists()
    
    
    def validate_email(email: str) -> bool:
        return not User.objects.filter(email).exists()
    

    def validate_phone_number(phone_number: str) -> bool:
        return not ContactInfo.objects.filter(phone_number=phone_number).exists()


    def validate_username_syntax(username: str) -> bool:
        return bool(re.match(REGEX['username'], username))
    

    def validate_email_syntax(email: str) -> bool:
        checks = (
            int('@' in email and email.count('@') == 1),
            int('.' in email.split('@')[1])
        )
        
        return True if len(checks) == sum(checks) else False


    def validate_bd_phone_number_syntax(phone_number: str) -> bool:
        _pn = re.sub(REGEX['space_sub'], '', phone_number) 
        checks = (
            int(_pn.startswith('+88') or _pn.startswith('01')),
            int(len(_pn.split('+88')) == 1),
            int(len(_pn.split('+88')[0]) == 11),
        )

        return True if len(checks) == sum(checks) else False


    def validate_gender(gender: str) -> bool:
        return gender in ['Male', 'Female', 'Other']


    def validate_birth_year(birth_year: int):
        from datetime import datetime
        year = datetime.today().year
        
        return birth_year < year - 13
