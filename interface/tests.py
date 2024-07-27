from django.contrib.auth.models import User
from .therapists.profile import TherapistProfile as TP
from .therapists.info import TherapistDisplayPrice as TDP
from therapy.models import TherapyType as TT, TherapyTypeMember as TTM
from therapists.models import Therapist
from schedules.models import TherapistSchedule as TS
import json


therapist = Therapist.objects.all().first()
user = User.objects.get(username='mumitprottoy')
therapy_type = TT.objects.get(code_name=1)

def ttp():
    profile = TP(therapist, therapy_type)
    print(json.dumps(profile.for_client(user), indent=2))


def ttdp():
    tdp = TDP(therapist)
    print(json.dumps(tdp.prices, indent=2))
    

# def nice():
#     from requests import get as fetch
#     url = 'https://theyellowtherapist.com/data/schedules'
#     response = fetch(url)
#     if response.status_code == 200:
#         schedules = response.json()['data']
#         for schedule in schedules:
#             if User.objects.filter(username=schedule['handle']).exists():
#                 user = User.objects.get(username=schedule['handle'])
#                 if Therapist.objects.filter(user=user).exists():
#                     hour, minute = schedule['time'].split(':')
#                     kwargs = {
#                         'therapist': Therapist.objects.get(user=user),
#                         'weekday': {
#                             'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
#                             'Thursday': 3, 'Friday': 4, 'Saturday': 5,
#                             'Sunday': 6
#                         }[schedule['weekday']],
#                         'hour': int(hour),
#                         'minute': int(minute)
#                     }
#                     if not TS.objects.filter(**kwargs).exists():
#                         TS(**kwargs).save()
#                         kwargs['therapist'] = kwargs['therapist'].user.username
#                         print(f'\nSaved: {json.dumps(kwargs, indent=4)}\n')
    
