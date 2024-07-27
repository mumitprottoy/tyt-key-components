import os 

email_creds = {
    'accounts': {
        'email': os.environ['TYT_ACC_EMAIL_ADDR'],
        'password': os.environ['TYT_ACC_EMAIL_PWD'],
    },
    'appointments': {
        'email': os.environ['TYT_APNT_EMAIL_ADDR'],
        'password': os.environ['TYT_APNT_EMAIL_PWD'],
    },
    'operations': {
        'email': os.environ['TYT_OPS_EMAIL_ADDR'],
        'password': os.environ['TYT_OPS_EMAIL_PWD'],
    }

}

office_email = email_creds['operations']['email']

def get_cred(email_type: str):
    creds = email_creds[email_type]

    class Cred:
        address = creds['email']
        password = creds['password']
    
    return Cred()