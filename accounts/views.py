from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

def auth_status(request):
    return render(request, 'accounts/auth_checker.html')


@csrf_exempt
def cross_authenticate(request):
    print('POST Data:', request.POST)
    if request.POST:
        user = User.objects.get(id=int(request.POST['user_id']))
        login(request, user)
        return redirect('auth-checker')
    