from django.contrib.auth.models import User
from therapists.models import Therapist
from therapy.models import TherapyType
from .info import TherapistBasicInfo, TherapistDisplayPrice
from ..payment.preview import PaymentPreview
from schedules.slot_generator import Slotter



class TherapistProfile:

    def __init__(self, therapist: Therapist, therapy_type: TherapyType) -> None:
        self.therapist = therapist
        self.therapy_type = therapy_type
    

    def __basic_info(self):
        return TherapistBasicInfo(self.therapist).__dict__
    

    def __get_base_display_price(self):
        return TherapistDisplayPrice(
            self.therapist, self.therapy_type).prices[self.therapy_type.readable_name]
    

    def __get_client_specific_price(self, client: User):
        preview = PaymentPreview(
            therapist=self.therapist, user=client, therapy_type=self.therapy_type)
        payment_info = preview.bipolar_payment_info.minimum
        return {
            'display_price': payment_info.display_price,
            'is_discounted': payment_info.is_discounted,
            'applied_discount': payment_info.applied_discount,
            'payable_amount': payment_info.payable_amount,
        }
    

    def for_public(self):
        profile = self.__basic_info()
        profile.update(self.__get_base_display_price())

        return profile
    

    def for_client(self, client: User):
        profile = self.__basic_info()
        profile.update(self.__get_client_specific_price(client))
        profile['slots'] = Slotter(
            therapist=self.therapist).generate_slots(as_str=True, client=client)

        return profile

            
