from django.db import models
from therapists.models import Therapist
from utils.constants import WEEKDAYS_ABBR



class TherapistSchedule(models.Model):
    
    """ 
    Found out in PYPI that calendar module is depricated.
    So had to hard code weekday tuple to generate choices.
    """
    WEEKDAY_CHOICES = tuple(
        (index, day) for index, day in enumerate(WEEKDAYS_ABBR)
    )
    
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=0)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    is_active = models.BooleanField(verbose_name="Active", default=True)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['therapist', 'weekday', 'hour', 'minute'],
                name= 'unique_schedule'
            )
        ]
    
    
    def __str__(self):
        return self.therapist.user.username
