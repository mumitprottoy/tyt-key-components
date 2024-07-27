import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def post_data(request):
    resp_dict = {'message': 'hi'}
    try:
        if request.body:
            body = request.body.decode('utf-8')
            _dict = json.loads(body)
            file = open('error.txt', 'w', encoding='utf-8')
            file.write(json.dumps(_dict, indent=4, ensure_ascii=False)); file.close()

            resp_dict['message'] = 'posted'

        return JsonResponse(resp_dict)
    except Exception as e:
        file = open('post_error.txt', 'w', encoding='utf-8')
        file.write(str(e)); file.close()