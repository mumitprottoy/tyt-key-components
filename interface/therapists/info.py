from therapists.models import *
from therapy.models import TherapyType, TherapyTypeMember
from accounts.models import ContactInfo
from finances.models import (
    PriceGroup, PriceGroupTherapistMember, BaseSessionFee)




class TherapistBasicInfo:
     
     def __init__(self, therapist: Therapist) -> None:
        self.id = therapist.id
        self.name = therapist.user.get_full_name()
        self.experience = TherapistExperience.objects.get(
            therapist=therapist).get_experience()
        self.experience_str = TherapistExperience.objects.get(
            therapist=therapist).get_experience_str()
        self.offered_therapy_types = [
            ttm.therapy_type.readable_name for ttm in TherapyTypeMember.objects.filter(
                therapist=therapist)]
        self.profile_pic_url = TherapistProfilePicture.objects.get(
            therapist=therapist).url
        self.expertise = [
            xpts.field.name for xpts in TherapistExpertise.objects.filter(
                therapist=therapist)]
        self.workplaces = [
            wp.workplace for wp in TherapistWorkplace.objects.filter(
                therapist=therapist)]
        self.qualifications = [
            q.qualification for q in TherapistQualification.objects.filter(
                therapist=therapist)]
        self.meeting_link = TherapistMeetingLink.objects.get(
            therapist=therapist).link



class TherapistContactInfo:

    def __init__(self, therapist :Therapist) -> None:
        self.email = therapist.user.email
        self.phone_number = ContactInfo.objects.get(
            user=therapist.user).phone_number



class TherapistDisplayPrice:

    def __init__(self, therapist: Therapist, therapy_type: TherapyType) -> None:
        self.therapist = therapist
        self.therapy_type = therapy_type
        self.prices: dict = self.__get_all_display_prices() 
    

    def __calculate_display_price(
            self, base_fee: int, commission: int, discount: int):
        base_fee = base_fee - (base_fee * discount/100)
        return base_fee + (base_fee * commission/100)


    def __get_display_price(
            self, base_fee: BaseSessionFee, pgtm: PriceGroupTherapistMember):
        prices = dict(); commission = pgtm.group.commission

        for session in ['first_session', 'recurring_session']:
            prices[session] = self.__calculate_display_price(
                base_fee=base_fee.__dict__[session],
                commission=commission.__dict__[session],
                discount=pgtm.__dict__[session+'_therapist_discount']
            )
        
        return prices


    def __get_all_display_prices(self):
        prices = dict()
        base_fee = BaseSessionFee.objects.get(
            therapist=self.therapist, therapy_type=self.therapy_type)

        for pg in PriceGroup.objects.filter(therapy_type=self.therapy_type):
            for pgtm in PriceGroupTherapistMember.objects.filter(
                group=pg, therapist=self.therapist):
                if not self.therapy_type.readable_name in prices: 
                    prices[self.therapy_type.readable_name] = {}
                display_price = self.__get_display_price(
                    base_fee=base_fee, 
                    pgtm=pgtm
                )
                prices[self.therapy_type.readable_name][
                    pgtm.group.name] = display_price


        return prices
