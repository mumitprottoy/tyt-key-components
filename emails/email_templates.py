templates = {
    'verify_email': {
        'email_type': 'accounts',
        'subject': 'Verification Code',
        'html': 'emails/verification_code.html'
    },

    'reset_password': {
        'email_type': 'accounts',
        'subject': 'Your OTP',
        'html': 'emails/reset_password.html',
    },

    'welcome': {
        'email_type': 'accounts',
        'subject': 'Welcome to TYT!',
        'html': 'emails/welcome.html'
    },
    
    'confirm_appointment': {
        'email_type': 'appointments',
        'subject': 'New Appointment Booked!',
        'html': 'emails/appointment_confirmed.html'
    },
    'appointment_reminder': {
        'email_type': 'appointments',
        'subject': 'Appointment Reminder',
        'html': 'emails/appointment_reminder.html'
    }
}



def inject_code_in_subject(subject: str, subject_code: str):
    return f'{subject} [{subject_code}]'


class EmailTemplate:
    email_type: str
    subject: str
    html: str
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(**kwargs)
        
        
def get_template(operation: str, subject_code: str=str()) -> EmailTemplate:
    op = templates[operation].copy()
    if subject_code:
        op['subject'] = inject_code_in_subject(op['subject'], subject_code)

    return EmailTemplate(**op)
