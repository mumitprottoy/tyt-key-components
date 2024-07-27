from django.http import JsonResponse
from therapy.models import TherapyType, therapy_type_data
from utils.operations import get_serializable_dict
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def serve_therapy_types(request):
    therapy_types: list[dict] = list()
    for tt in TherapyType.objects.all():
        _dict = get_serializable_dict(tt, pop_id=True)
        _dict.update(therapy_type_data[tt.code_name])
        therapy_types.append(_dict)
    return JsonResponse(
        data={'therapy_types': therapy_types}, status=200)
    
    

