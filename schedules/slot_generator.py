from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import TherapistSchedule, Therapist
from utils.constants import SLOT_DATETIME_FORMAT
from utils.operations import make_datetime_aware
from appointments.models import Appointment



# Slotter/Slaughter: checks a given slot's validity and generates new ones
class Slotter:

    def __init__(self, therapist:Therapist):
        self.therapist = therapist
        self.schedules = TherapistSchedule.objects.filter(therapist=therapist).all()
        
      
    """ 
    The following __dates() function takes a 
    weekday (e.g Monday) as int and returns 
    the next date that has the same weekday 
    based on the day it is called in. 
    Returns all the dates within a range called window.

    Example: 
    If the given weekday is Friday and the date this function
    is called is Nov 11, Wednesday, and a 7 days window - it 
    returns the date Nov 13, Friday and returns only one
    date because there is only one Friday within the given 
    window of 7 days.
    """
    def __dates(self, weekday:int, hour:int, minute:int, window:int=15) -> list[datetime]:
        dates = list()
        today = datetime.today()
        SE7EN = 7  # 7 days a week
        x = weekday; y = today.weekday()
        date_difference = ((x - (y + 1)) % SE7EN) + 1

        while date_difference < window:
            next_date = (today + timedelta(date_difference)).replace(
                hour=hour, 
                minute=minute,
                second=0
            )
            next_date = make_datetime_aware(next_date)
            if self.slot_is_valid(next_date): dates.append(next_date)
                
            date_difference += SE7EN

        return dates


    def __kwargs(self, schedule: TherapistSchedule) -> dict:
        schedule: dict = schedule.__dict__.copy()
        for key in ['_state', 'id', 'therapist_id', 'is_active']:
            schedule.pop(key)
        
        return schedule


    def generate_slots(self, window:int=15, as_str:bool=False, client=None) -> list:
        slots: list[datetime] = list()
        for schedule in self.schedules:
            for slot in self.__dates(
                window=window, **self.__kwargs(schedule=schedule)):
                """
                Weirdly enough, neither of list.sort() 
                or sorted(list) seem to be working
                on list[datetime]. I really have no idea why.
                So, sorting manually, on the fly.
                """
                i = len(slots) - 1; slots += [0]
                while i >= 0 and slots[i] > slot:
                    slots[i+1] = slots[i]; i -= 1
                slots[i+1] = slot                   
        if client is not None:
            _slots: list[dict] = list()
            if Appointment.objects.filter(client=client).exists():
                apnt = Appointment.objects.order_by('-slot').filter(client=client).first()
                from django.utils import timezone
                if timezone.is_naive(apnt.slot):
                    apnt.slot = make_datetime_aware(apnt.slot)
                    apnt.save()
                for slot in slots:
                    if (slot - apnt.slot).total_seconds() > 3600 * 2:
                        _slots.append(slot)
                slots = _slots.copy()

        if as_str:
            for i in range(len(slots)): 
                slots[i] = slots[i].strftime(SLOT_DATETIME_FORMAT)
        
        return slots             
        


    def slot_is_valid(self, date_time:datetime) -> bool:
        x = TherapistSchedule.objects.filter(
            therapist=self.therapist,
            weekday=date_time.weekday(),
            hour=date_time.hour,
            minute=date_time.minute
        ).exists()

        y = not Appointment.objects.filter(
            therapist=self.therapist,
            slot=date_time
        ).exists()

        return x and y
    

        
    def convert_str_to_datetime(
            self, datetime_str:str, fmt:str=SLOT_DATETIME_FORMAT) -> datetime:
        try: return datetime.strptime(datetime_str, fmt)
        except ValueError: return None
