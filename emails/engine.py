from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from . import constants as const 
from .creds import get_cred, office_email
from .email_templates import get_template



class EmailEngine:

    def __init__(
            self, 
            recipient_list: list, 
            operation: str, 
            context: dict=dict(), 
            subject_code: str=str(), 
            notify_office: bool=False, 
            fail_silently: bool=True) -> None:
                
        self.template = get_template(operation, subject_code)
        self.cred = get_cred(self.template.email_type)
        self.context = context
        self.recipient_list = recipient_list
        if notify_office and office_email not in self.recipient_list:
            self.recipient_list.append(office_email)
        self.fail_silently = fail_silently
        
        
    
    def __connect(self):
        return get_connection(
            host=const.HOST,
            port=const.PORT,
            user_tls=const.USE_TLS,
            username=self.cred.address,
            password=self.cred.password
        )


    def __process_message(self):
        connection = self.__connect()
        html_message = render_to_string(self.template.html, self.context)
        message = strip_tags(html_message)
        return {
            'subject': self.template.subject,
            'from_email': self.cred.address,
            'recipient_list': self.recipient_list,
            'message': message,
            'html_message': html_message,
            'connection': connection,
            'fail_silently': self.fail_silently
        }


    def send(self):
        kwargs = self.__process_message()
        send_mail(**kwargs)
