from . import constants as const 
from finances.models import Invoice


def get_payload(invoice: Invoice) -> dict:
    payload = {
        "isSandbox" : False,
        "storeID" : const.store_id,
        "successUrl" : const.return_url+invoice.tracker.key,
        "failUrl" : const.return_url+invoice.tracker.key,
        "cancelUrl" : const.return_url+invoice.tracker.key,
        "transactionID" : invoice.transaction_id,
        "transactionAmount" : invoice.amount,
        "signature" : const.signature_key,
        "customerState" : invoice.tracker.key,
        "customerName" : invoice.client.get_full_name(),
        "customerEmail" : invoice.client.email,
        "customerMobile" : invoice.client.contactinfo.phone_number
    }

    return payload