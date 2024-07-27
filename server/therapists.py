from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import UserGroup, UserGroupMember
from interface.therapists.profile import Therapist, TherapyType, TherapistProfile
from django.views.decorators.csrf import csrf_exempt
from utils import decorators, operations


# public endpoint
@csrf_exempt
def serve_therapists_for_public(request, code_name: int) -> JsonResponse:
    profiles: list[dict] = list()
    therapy_type = TherapyType.objects.get(code_name=int(code_name))

    for therapist in Therapist.objects.filter(is_public=True).all():
        profile = TherapistProfile(therapist, therapy_type)
        profiles.append(profile.for_public())

    return JsonResponse({'therapists': profiles}) 
    
    
@csrf_exempt
@decorators.private
@decorators.post_data_required
def serve_all_therapists_for_client(request, **kwargs) -> JsonResponse:
    body = operations.dict_to_object(kwargs['body']['data'])
    code_name = body.code_name; user_id = body.user_id
    
    profiles: list[dict] = list()
    user = User.objects.get(id=int(user_id))
    office = UserGroup.objects.get(name='Office')
    therapy_type = TherapyType.objects.get(code_name=int(code_name))
    therapists = Therapist.objects.filter(is_public=True).all()
    
    if UserGroupMember.objects.filter(group=office, member=user).exists():
        therapists = Therapist.objects.all()
        
    for therapist in therapists:
        if user.id != therapist.user.id:
            profile = TherapistProfile(therapist, therapy_type)
            profiles.append(profile.for_client(user))
            
    return JsonResponse({'therapists': profiles}) 
    
   
@csrf_exempt
@decorators.private
@decorators.post_data_required
def serve_therapist_for_client(request, **kwargs) -> JsonResponse:
    body = operations.dict_to_object(kwargs['body']['data'])
    user_id = body.user_id, code_name = body.code_name, therapist_id = body.therapist_id
    
    client = User.objects.get(id=int(user_id))
    therapy_type = TherapyType.objects.get(code_name=int(code_name))
    therapist = Therapist.objects.get(id=int(therapist_id))
    profile = TherapistProfile(therapist, therapy_type)

    return JsonResponse({'therapist': profile.for_client(client)})
