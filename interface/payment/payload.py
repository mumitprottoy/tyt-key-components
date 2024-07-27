from utils import constants as const 
from finances.models import Invoice


def get_payload(invoice: Invoice) -> dict:
    payload = {
        "isSandbox" : False,
        "storeID" : const.STORE_ID,
        "successUrl" : const.PAYMENT_RETURN_BASE_URL+invoice.tracker.key,
        "failUrl" : const.PAYMENT_RETURN_BASE_URL+invoice.tracker.key,
        "cancelUrl" : const.PAYMENT_RETURN_BASE_URL+invoice.tracker.key,
        "transactionID" : invoice.transaction_id,
        "transactionAmount" : invoice.amount,
        "signature" : const.SIGNATURE_KEY,
        "customerState" : invoice.tracker.key,
        "customerName" : invoice.client.get_full_name(),
        "customerEmail" : invoice.client.email,
        "customerMobile" : invoice.client.contactinfo.phone_number
    }

    return payload