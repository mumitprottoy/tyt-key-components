from django.contrib.auth.models import User
from appointments.models import Appointment
from therapists.models import TherapistProfilePicture as TPP
from utils.constants import SLOT_DATETIME_FORMAT as SDF
from utils.operations import make_datetime_aware as mda
from datetime import datetime



class AppointmentInfo:
    
    def __init__(self, user: User) -> None:
        self.user = user
        self.appointments = self.__get_all_apnts()
        self.count = len(self.appointments)
        self.recent_appointment = self.__get_most_recent_apnt()
        
    
    def __get_all_apnts(self) -> list[dict]:
        apnts: list[dict] = list()
        
        for apnt in Appointment.objects.filter(client=self.user).order_by('-slot'):
            therapist_pic_url = TPP.objects.get(therapist=apnt.therapist).url
            apnts.append({
                'tracker_key': apnt.tracker.key,
                'therapist_full_name': apnt.therapist.user.get_full_name(),
                'therapist_pic_url': therapist_pic_url,
                'slot': apnt.slot.strftime(SDF),
                'is_free': apnt.is_free,
                'session_completed': apnt.session_completed
            })
        
        return apnts
    
    
    def __get_most_recent_apnt(self):
        apnt = Appointment.objects.filter(
            client=self.user, session_completed=False).order_by('-slot').first()
        therapist_pic_url = TPP.objects.get(therapist=apnt.therapist).url
        '''
        The highest possible time difference between any two timezones
        is 26 hours or 26 * 3600 seconds (that's a fact)
        '''
        time_gap = 26 * 3600
        return {
            'tracker_key': apnt.tracker.key,
            'therapist_full_name': apnt.therapist.user.get_full_name(),
            'therapist_pic_url': therapist_pic_url,
            'meeting_link': apnt.link
        } if (mda(datetime.today()) - mda(apnt.slot)).total_seconds() < time_gap else None
        