email_creds = {
    'accounts': {
        'email': 'accounts@theyellowtherapist.com',
        'password': 'em@ilaccountstyt',
    },

    'appointments': {
        'email': 'appointments@theyellowtherapist.com',
        'password': 'em@ilappointmentstyt',
    },

    'operations': {
        'email': 'operations@theyellowtherapist.com',
        'password': 'operationstytweb',
    }

}



office_email = email_creds['operations']['email']

def get_cred(email_type: str):
    creds = email_creds[email_type]

    class Cred:
        address = creds['email']
        password = creds['password']
    
    return Cred()