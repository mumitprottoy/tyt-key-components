from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from therapists.models import Therapist, TherapistMeetingLink
from therapy.models import TherapyType
from utils.models import Tracker
from utils.operations import make_datetime_aware
from utils.constants import APNT_HOLD_LIMIT as ahl



class Appointment(models.Model):
    FIRST_SESSION = 'First Session'; RECURRING_SESSION = 'Recurring Session'
    SESSION_TYPE_CHOICES = (
        (FIRST_SESSION, FIRST_SESSION),
        (RECURRING_SESSION, RECURRING_SESSION)
    )

    PENDING = 'Pending'; CONFIRMED = 'Confirmed'
    STATUS_CHOICES = (
        (PENDING, PENDING), (CONFIRMED, CONFIRMED)
    )

    tracker = models.OneToOneField(Tracker, on_delete=models.CASCADE)
    therapy_type = models.ForeignKey(TherapyType, on_delete=models.DO_NOTHING)
    therapist = models.ForeignKey(Therapist, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    """
    Slot objects are subject to cleanups.
    So using DateTimeField instead, 
    to avoid post-mistake-catastrophe.
    """
    slot = models.DateTimeField()

    link = models.ForeignKey(TherapistMeetingLink, on_delete=models.DO_NOTHING)
    session_type = models.CharField(
        max_length=20, choices=SESSION_TYPE_CHOICES, default=FIRST_SESSION)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_free = models.BooleanField(default=False)
    session_completed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    

    def get_slot_str(self):
        from utils.constants import SLOT_DATETIME_FORMAT
        return self.slot.astimezone(timezone.get_current_timezone()).strftime(SLOT_DATETIME_FORMAT)
    

    def get_secs_past(self):
        from datetime import datetime
        today = datetime.today().astimezone(self.booked_at.tzinfo)
        return int((today - self.booked_at).total_seconds())+1


    def get_hold_secs_left(self):
        if self.status == self.PENDING:
            secs_left = int(ahl) - self.get_secs_past()
            return secs_left if secs_left > 0 else 0
        return None
    
    
    def get_hold_secs_left_for_client(self):
        if self.status == self.PENDING:
            secs_left = int(ahl/2) - self.get_secs_past()
            return secs_left if secs_left > 0 else 0
        return None


    def get_slot_secs_left(self):
        if not self.session_completed:
            import math
            from datetime import datetime
            today = datetime.today().astimezone(self.slot.tzinfo)
            secs_left = math.floor((self.slot - today).total_seconds())
            return secs_left
        return None
    

    def get_hold_secs_left_script(self):
        return f'<script>let holdSecsLeft = {self.get_hold_secs_left_for_client()}; </script>'
    
    
    def get_slot_secs_left_script(self):
        secs_left  = self.get_slot_secs_left()
        secs_left = secs_left if secs_left > 0 else 0
        return f'<script>let slotSecsLeft = {secs_left}; </script>'


    def validate_not_same_person(self):
        if self.therapist.user == self.client:
            from utils.exceptions import TherapistClientSamePersonError
            raise TherapistClientSamePersonError(
                'A therapist cannot book its own appointment.')
    
    
    def clean(self):
        self.validate_not_same_person()
    
    
    def confirm(self):
        self.status = self.CONFIRMED
        if self.tracker.invoice.amount == 0:
            self.is_free = True
        self.save()
    

    def save(self, *args, **kwargs):
        if timezone.is_naive(self.slot):
            self.slot = make_datetime_aware(self.slot)
            
        super().save(*args, **kwargs)

    
    class Meta:
        """
        Same client booking multiple appointments at 
        the same slot (different therapists)
        """
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'slot'],
                name='multiple_same_date_time_appointment' 
            )
        ]


    def __str__(self):
        return self.tracker.key
    


    
    
         