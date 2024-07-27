from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from utils.decorators import private, post_data_required
from entrance.operations import create_user, authenticate_user


@csrf_exempt
@private
@post_data_required
def signup(request, *args, **kwargs):
    body = kwargs['body']
    response = create_user(body['data'], body['csrf'])

    return JsonResponse(response, status=200)



@csrf_exempt
@private
@post_data_required
def login(request, *args, **kwargs):
    body = kwargs['body']
    response = authenticate_user(body['data'], body['csrf'])

    return JsonResponse(response, status=200)