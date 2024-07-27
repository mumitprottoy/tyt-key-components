import requests
from django.shortcuts import redirect
from django.contrib.auth.models import User
from utils.operations import resolve_trx_check_url as rtcu
from utils.constants import API_TOKEN
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from utils.models import Tracker
from utils.operations import resolve_apnt_url as rau
from appointments.models import Appointment
from interface.appointment.info import AppointmentInfo as AI




def _get_apnt_dict(apnt: Appointment) -> dict:
    return {
        'id': apnt.id,
        'tracker_key': apnt.tracker.key,
        'client_id': apnt.client.id,
        'client_name': apnt.client.get_full_name(),
        'client_profile_picture_url': apnt.client.profilepicture.url,
        'therapist_id': apnt.therapist.id,
        'therapist_name': apnt.therapist.user.get_full_name(),
        'therapist_profile_picture_url': apnt.therapist.therapistprofilepicture.url,
        'slot': apnt.get_slot_str(),
        'secs_past': apnt.get_secs_past(),
        'hold_secs_left': apnt.get_hold_secs_left(),
        'hold_secs_left_for_client': apnt.get_hold_secs_left_for_client(),
        'hold_secs_left_script': apnt.get_hold_secs_left_script(),
        'slot_secs_left': apnt.get_slot_secs_left(),
        'slot_secs_left_script': apnt.get_slot_secs_left_script(),
        'session_fee': apnt.tracker.invoice.amount,
        'is_free': apnt.is_free,
        'status': apnt.status,
        'session_completed': apnt.session_completed,
        'session_type': apnt.session_type,
        'meeting_link': apnt.link.link
    } if apnt is not None else apnt



@csrf_exempt
def get_all_appointments_by_user_id(request, token, user_id):
    if token == API_TOKEN:
        client = User.objects.get(id=int(user_id))
        apnts = list()
        for apnt in Appointment.objects.order_by('slot').filter(client=client).all():
            if apnt.status == Appointment.PENDING:
                response = requests.get(rtcu(apnt.tracker.invoice.transaction_id)).json()
                if 'pay_status' in response and response['pay_status'] == 'Successful':
                    apnt.tracker.invoice.close_transaction()
                    apnt.status = Appointment.CONFIRMED; apnt.save()
            apnts.append(_get_apnt_dict(apnt))
        
        return JsonResponse({'appointments': apnts})


@csrf_exempt
def get_appointment_by_id(request, token, apnt_id):
    if token == API_TOKEN:
        apnt = Appointment.objects.get(
            id=int(apnt_id)) if Appointment.objects.filter(
                id=int(apnt_id)).exists() else None
        
        if apnt is not None:
            response = requests.get(rtcu(apnt.tracker.invoice.transaction_id)).json()
            if 'pay_status' in response and response['pay_status'] == 'Successful':
                apnt.tracker.invoice.close_transaction()
                apnt = apnt.tracker.appointment
        
        return JsonResponse({'appointment': _get_apnt_dict(apnt)})
        
        
@csrf_exempt
def check_slot_validity(request, slot):
    from datetime import datetime
    from utils.constants import SLOT_ARG_FORMAT
    from utils.operations import make_datetime_aware
    
    slot = make_datetime_aware(datetime.strptime(str(slot), SLOT_ARG_FORMAT))
    is_valid = True; error_message = list()
    if Appointment.objects.filter(slot=slot).exists():
        is_valid = False; error_message = ['This slot is already taken, please choose a different one.']
    
    return JsonResponse({'is_valid': is_valid, 'error_message': error_message})
        
    
    
@csrf_exempt
def book_appointment(request, token, user_id, code_name, therapist_id, slot):
    if token == API_TOKEN:
        from interface.appointment.processor import (
            AppointmentProcessor, BookingArgumentProcessor)
        kwargs = BookingArgumentProcessor(user_id, therapist_id, code_name, slot).get_kwargs()
        processor = AppointmentProcessor(**kwargs)
        apnt = processor.book()
        return JsonResponse({'appointment': _get_apnt_dict(apnt)})


@csrf_exempt
def check_for_pending_appointment(request, token, user_id):
    if API_TOKEN == token:
        user = User.objects.get(id=int(user_id))
        if Appointment.objects.filter(client=user, status=Appointment.PENDING).exists():
            apnt = Appointment.objects.get(client=user, status=Appointment.PENDING)
            response = {'exists': True, 'apnt_id': apnt.id}
        else: response = {'exists': False}

        return JsonResponse(response)
