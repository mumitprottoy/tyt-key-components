from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from utils.decorators import private, post_data_required
from utils.operations import dict_to_object
from emails.engine import EmailEngine
from accounts.models import MagicKey




@csrf_exempt
@private
@post_data_required
def send_verification_code(request, *args, **kwargs):
    try:
        data = dict_to_object(kwargs['body']['data'])
        user = User.objects.get(id=data.user_id)
        code = user.verificationcode.code
        context = {'code': code}
        email = EmailEngine(
            [user.email], 'verify_email', context, subject_code=code)
        email.send()
        return JsonResponse({'success': True}, status=200)
    
    except Exception as exec:
        print(exec); return JsonResponse({}, status=500)
    

@csrf_exempt
@private
@post_data_required
def send_otp(request, *args, **kwargs):
    try:
        data = dict_to_object(kwargs['body']['data'])
        user = User.objects.get(id=data.user_id)
        otp = user.otp.code
        context = {'otp': otp}
        email = EmailEngine(
            [user.email], 'reset_password', context, subject_code=otp)
        email.send()
        return JsonResponse({'success': True}, status=200)
    
    except Exception as exec:
        print(exec); return JsonResponse({}, status=500)


    