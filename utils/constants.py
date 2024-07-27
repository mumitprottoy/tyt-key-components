import os

FORM_FIELDS = {
    'signup': ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password'],
    'signin': ['username_or_email', 'password']
}
PAYMENT_BASE_URL = os.environ['TYT_PAYEMENT_BASE_URL']
SIGNATURE_KEY = os.environ['TYT_SIGN_KEY']
STORE_ID = os.environ['TYT_STORE_ID']
PAYMENT_RETURN_BASE_URL = os.environ['TYT_PAYEMENT_RETURN_URL']
TRX_CHECK_BASE_URL = os.environ['TYT_TRXN_CHECK_BASE_URL']
APNT_BASE_URL = os.environ['TYT_APNT_BASE_URL']
API_TOKEN = os.environ['TYT_PRIVATE_API_TOKEN']
APNT_HOLD_LIMIT = int(os.environ['TYT_APNT_HOLD_LIMIT'])


SLOT_DATETIME_FORMAT = '%d %b, %Y %a %H:%M'
DATETIME_FORMAT_FOR_KEYS = '%f%y%m%d%M%H%S'
SLOT_ARG_FORMAT = '%y%m%d%H%M%S'

REGEX = {
    'username': r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$',
    'name_sub': r'[^a-zA-Z\s]',
    'name': r'^[a-zA-Z.\s]',
}


