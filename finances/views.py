import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from utils.models import Tracker
from utils.operations import resolve_apnt_url as rau, resolve_trx_check_url as rtcu
from utils.constants import API_TOKEN as token
from .models import Invoice
from appointments.models import Appointment
from interface.payment.processor import PaymentProcessor



def payment(request, tracker_key: str):
    tracker = Tracker.objects.get(key=str(tracker_key))

    if not tracker.invoice.is_closed:
        response = requests.get(rtcu(tracker.invoice.transaction_id)).json()
        if 'pay_status' in response and response['pay_status'] == 'Successful':
            tracker.invoice.close_transaction()
        else:
            processor = PaymentProcessor(tracker=tracker)
            gateway = processor.request_gateway()
            return redirect(gateway)
    
    return redirect(rau('poiuytrewq', token, tracker.invoice.client.id, tracker.appointment.id))



@csrf_exempt
def payment_return(request, tracker_key):
    tracker = Tracker.objects.get(key=tracker_key)
    if request.POST:
        if request.POST['pay_status'] == 'Successful':
            tracker.invoice.close_transaction()

    return redirect(rau('poiuytrewq', token, tracker.invoice.client.id, tracker.appointment.id))



@csrf_exempt
def payment_event_notification(request):
    if request.POST:
        tracker_key = request.POST['desc']
        tracker = Tracker.objects.get(key=tracker_key)
        apnt = Appointment.objects.get(tracker=tracker)
        if request.POST['pay_status'] == 'Successful':
            invoice = Invoice.objects.get(tracker=tracker)
            invoice.is_closed = True; invoice.save()



