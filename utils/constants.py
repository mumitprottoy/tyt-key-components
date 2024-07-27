FORM_FIELDS = {
    
    'signup': [
        'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password'
    ],
    
    'signin': [
        'username_or_email', 'password'
    ]
}
PAYMENT_BASE_URL = 'https://secure.aamarpay.com/jsonpost.php'
SIGNATURE_KEY = 'bd32dd400c563ceeeceb60faf2a9efeb'
STORE_ID = 'theyellowtherapist'
PAYMENT_RETURN_BASE_URL = 'https://api.theyellowtherapist.com/payment-return/'
TRX_CHECK_BASE_URL = "https://secure.aamarpay.com/api/v1/trxcheck/request.php?"
APNT_BASE_URL = 'https://appointments.theyellowtherapist.com/'
API_TOKEN = '@570Z703ZRGK'
APNT_HOLD_LIMIT = 3600
WEEKDAYS_ABBR = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


SLOT_DATETIME_FORMAT = '%d %b, %Y %a %H:%M'
DATETIME_FORMAT_FOR_KEYS = '%f%y%m%d%M%H%S'
SLOT_ARG_FORMAT = '%y%m%d%H%M%S'

REGEX = {
    'username': r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$',
    'name_sub': r'[^a-zA-Z\s]',
    'name': r'^[a-zA-Z.\s]',
}


