from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from therapists.models import Therapist, TherapistMeetingLink
from schedules.slot_generator import Slotter
from therapy.models import TherapyType, TherapyTypeMember
from therapy.models import TherapyType
from interface.payment.preview import PaymentPreview
from finances.models import Invoice, PaymentInfo
from utils.constants import SLOT_ARG_FORMAT as saf
from appointments.models import Appointment
from utils.models import Tracker



class AppointmentProcessor:

    def __init__(
            self, therapist: Therapist, client: User, therapy_type: TherapyType, slot: datetime) -> None:
        self.client =  client
        self.therapist = therapist
        self.therapy_type = therapy_type
        self.slot = slot


    def __create_tracker(self) -> Tracker:
        key = Tracker.generate_tracker_key()
        tracker = Tracker(key=key)
        tracker.save()
        
        return tracker

    
    def book(self) -> Appointment:
        tracker = self.__create_tracker()
        preview = PaymentPreview(
            therapist=self.therapist,
            user=self.client, 
            therapy_type=self.therapy_type
        )
        
        payment_info = PaymentInfo(**preview.bipolar_payment_info.minimum.__dict__)
        payment_info.client = self.client; payment_info.tracker = tracker
        invoice = Invoice(tracker=tracker, client=self.client)

        if payment_info.is_payable: 
            invoice.amount = payment_info.payable_amount
        else: invoice.is_closed = True

        payment_info.save(); invoice.save()

        apnt = Appointment(
            tracker = tracker,
            therapy_type = self.therapy_type,
            therapist = self.therapist,
            client = self.client,
            link = TherapistMeetingLink.objects.get(
                therapist=self.therapist),
            slot = self.slot
        )

        if not payment_info.is_payable: apnt.is_free = True
        if invoice.is_closed: apnt.status = Appointment.CONFIRMED
        apnt.session_type = Appointment.RECURRING_SESSION if Appointment.objects.filter(
            therapist=self.therapist, client=self.client
        ).exists() else Appointment.FIRST_SESSION

        apnt.save()

        return apnt



class BookingArgumentProcessor:

    def __init__(
            self, user_id: int, therapist_id: int, code_name: int, slot_arg: int) -> None:
        self.user_id = user_id
        self.therapist_id = therapist_id
        self.code_name = code_name
        self.slot_str = str(slot_arg)
    
    def get_therapist(self):
        return Therapist.objects.get(id=self.therapist_id)
        
    
    def get_client(self):
        return User.objects.get(id=self.user_id)
        

    def get_slot(self): 
        slaughter = Slotter(self.get_therapist())
        slot_datetime = datetime.strptime(
            self.slot_str, saf).astimezone(timezone.get_current_timezone())

        return slot_datetime if slaughter.slot_is_valid(
            slot_datetime) else None
    

    def get_therapy_type(self):
        tt = TherapyType.objects.get(code_name=self.code_name)
        ttm = TherapyTypeMember.objects.get(
            therapist=self.get_therapist(), therapy_type=tt)

        return ttm.therapy_type
    

    def get_kwargs(self):
        return {
            'therapist': self.get_therapist(),
            'client': self.get_client(),
            'therapy_type': self.get_therapy_type(),
            'slot': self.get_slot()
        } 
        

