import json
from django.http import HttpResponse, JsonResponse
from .constants import API_TOKEN
from .operations import dict_to_object



def request_body_must_exist(func):
    
    def check(request, *args, **kwargs):
        if not request.body: 
            return HttpResponse('No view.')
        
        return func(request, *args, **kwargs)
    
    return check
            


def get_request_body_as_dict(request):
    # decode and convert into dict
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    return body
        



# Enpoints wrapped with this decorator can only be accessed with a private token
def private(endpoint):
    
    @request_body_must_exist
    def check(request, *args, **kwargs):
        body = get_request_body_as_dict(request)
        
        if 'token' in body:
            if body['token'] == API_TOKEN:
                return endpoint(request, *args, **kwargs)
        
        return JsonResponse({}, status=400)
           
    return check
    


def post_data_required(endpoint):
    
    @request_body_must_exist
    def check(request, *args, **kwargs):
        body = get_request_body_as_dict(request)
        
        if not 'data' in body:
            return JsonResponse({}, status=400)
        
        return endpoint(request, body=body)
    
    return check




    


