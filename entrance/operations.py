import re
from django.contrib.auth.models import User
from utils.form_validation import form_fields_are_valid
from utils.operations import get_rid_of_list_type_values
from .form_validation import validate_creds_from_signup_form
from utils.constants import FORM_FIELDS as ff




def filter_names(names: list[str]) -> list[str]:
    from utils.constants import REGEX as reg
    names  = [re.sub(reg['name_sub'], '', name) for name in names]

    for i in range(len(names)):
        parts = names[i].split()
        
        for j in range(len(parts)): 
            parts[j] = parts[j].lower().capitalize() 
    
        names[i] = ' '.join(parts)
    
    return names



def identify_username_or_email(cred:str):
    username, email = {"username": cred}, {"email": cred.lower()}
    
    if User.objects.filter(**username).exists():
        return True, username
    
    if User.objects.filter(**email).exists():
        return True, email
    
    return False, None



  
def get_prefill_context(form_data:dict, fields: list):
    context = form_data.copy()
    for f in fields: context[f] = ""
    context['password'] = context['confirm_password'] = str()
    
    return context



def extract_fields(status: tuple):
    return [issues[2] for issues in status[1] if len(issues)>2 and not issues[0]]

def extract_errors(status: tuple):
    return [issues[1] for issues in status[1]]
    



def create_user(form_data: dict, csrf=True) -> tuple[bool, str]:
    form_data = get_rid_of_list_type_values(form_data)
    status = form_fields_are_valid(
        inputs=list(form_data.keys()), fields=ff['signup'], csrf=csrf)
    
    if status[0]:
        form_data['first_name'], form_data['last_name'] = filter_names(
            [form_data['first_name'], form_data['last_name']])
        form_data['email'] = form_data['email'].lower()
        status = validate_creds_from_signup_form(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            username = form_data['username'],
            email = form_data['email'],
            password = form_data['password'],
            confirm_password = form_data['confirm_password']
        )

        if status[0]:

            pwd = form_data['password']
            form_data.pop('confirm_password')
            form_data.pop('password')
            if csrf: 
                form_data.pop('csrfmiddlewaretoken')
            new_user = User(**form_data)
            new_user.set_password(pwd)
            new_user.save()
            
            return {
                "success": True,
                "user_id": new_user.id
            }
        
        else: 
            return {
                "success": False,
                "errors": extract_errors(status),
                "prefill": {'prefill': get_prefill_context(form_data, extract_fields(status))}
            }
            
    
    return {
        "success": False,
        "errors": status[1]
    }

 
 

def authenticate_user(form_data: dict, csrf=True) -> tuple[bool, str]:
    form_data = get_rid_of_list_type_values(form_data)
    status = form_fields_are_valid(inputs=list(form_data.keys()), fields=ff['signin'], csrf=csrf)
    
    if status[0]:
        identified = identify_username_or_email(form_data['username_or_email'])
        
        if identified[0]:
            user: User = User.objects.get(**identified[1])
            
        else: 
            return {
                "success": False,
                "errors": ["User does not exist"]
            }
            
        
        from django.contrib.auth.hashers import check_password
        if check_password(form_data['password'], user.password):
            return {
                "success": True,
                "user_id": user.id
            }
        else: 
            return {
                "success": False,
                "errors": ['Wrong password'] 
            }
    
    return {
        "success": False,
        "errors": status[1]
    }
