from . import constants as const
from .payload import get_payload
from finances.models import Invoice
from utils.models import Tracker



class PaymentProcessor:

    def __init__(self, tracker: Tracker) -> None:
        self.tracker = tracker
        self.invoice = Invoice.objects.get(tracker=self.tracker)


    def request_gateway(self):
        if not self.invoice.is_closed:
            self.invoice.update_transaction_id()
            payload = get_payload(self.invoice)
            from aamarpay.aamarpay import aamarPay
            _ = aamarPay(**payload)
            return _.payment()
        
        return None
