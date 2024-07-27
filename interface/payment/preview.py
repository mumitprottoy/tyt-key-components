import math
from django.contrib.auth.models import User
from therapists.models import Therapist
from accounts.models import UserGroupMember
from finances.models import (
    BaseSessionFee, Commission, PriceGroup, PriceGroupTherapistMember, Promo, PromoRetrievalCount as PRC)
from appointments.models import Appointment
from therapy.models import TherapyType
from utils.operations import dict_to_object as ditto  


class PaymentPreview:
    
    def __init__(self, therapist: Therapist, user: User, therapy_type: TherapyType) -> None:
        self.user = user
        self.therapist = therapist
        self.therapy_type = therapy_type
        
        # computed attributes
        self.session_type = {
            True : 'recurring_session',
            False: 'first_session'
        }[Appointment.objects.filter(
            therapist=self.therapist, client=self.user).exists()]
        self.base_fee = BaseSessionFee.objects.get(
            therapist=self.therapist,
            therapy_type=self.therapy_type).__dict__[self.session_type]
        self.base_commission = Commission.objects.get(
            name='Base').__dict__[self.session_type]
        self.display_price = math.ceil(
            self.base_fee + self.base_fee * self.base_commission/100)
        self.payment_info = self.__get_payment_info()
        self.bipolar_payment_info = self.__get_bipolar_payment_info()
        self.payable_amount = self.bipolar_payment_info.minimum.payable_amount
        
    
    
    def __calc_price(self, therapist_discount:int, commission:int) -> int:
        b = self.base_fee; d = therapist_discount/100; c = commission/100
        p = b * (1 - d) * (1 + c)
        
        return math.ceil(p)
    
    
    
    def __calc_display_discount(self, payable_amount:int) -> int:
        discount = ((
            self.display_price - payable_amount) / self.display_price) * 100 
        
        return math.ceil(discount)
    
    
    def __get_applicable_promos(self):
        promos: list[Promo] = list()
        for promo in Promo.objects.filter(
            therapy_type=self.therapy_type, is_active=True):
            if UserGroupMember.objects.filter(
                    group=promo.user_group, member=self.user).exists():
                if bool(promo.user_retrieval_limit) and PRC.objects.get(
                        promo=promo, user=self.user).maxed_out:
                    continue
                promos.append(promo)
        
        return promos           
    
    
    def __get_payment_info(self):
        payment_info_list: list[dict] = list()

        for pg in PriceGroup.objects.filter(
            therapy_type=self.therapy_type, is_active=True).all():
            
            try:
                if UserGroupMember.objects.filter(
                    group=pg.user_group, member=self.user).exists():
                    therapist_discount = PriceGroupTherapistMember.objects.get(
                        group=pg, 
                        therapist=self.therapist
                    ).__dict__[self.session_type+'_therapist_discount']
                    therapist_due = math.ceil(
                        self.base_fee - self.base_fee * therapist_discount / 100)
                    commission = pg.commission.__dict__[self.session_type]
                    payable_amount = math.ceil(self.__calc_price(therapist_discount, commission) * 1.04)
                    applied_promo = None
                    for promo in self.__get_applicable_promos():
                        _amount = payable_amount - promo.max_deductable_amount
                        if promo.is_free or _amount < 0: _amount = 0
                        if _amount < payable_amount: 
                            payable_amount = _amount; applied_promo = promo
                        
                    payment_info_list.append(ditto({
                        'is_payable': payable_amount > 0,
                        'payable_amount': payable_amount,
                        'display_price': math.ceil(self.display_price * 1.04),
                        'payable_to_therapist': therapist_due,
                        'is_discounted': payable_amount < self.display_price,
                        'applied_discount': self.__calc_display_discount(payable_amount),
                        'applied_promo': applied_promo,
                        'applied_price_group': pg,
                        'applied_user_group': pg.user_group,
                        'applied_commission': commission
                    }))
            except PriceGroupTherapistMember.DoesNotExist:
                continue
        
        
        return payment_info_list


    def __get_bipolar_payment_info(self) -> object:
        info = dict()
        payment_info_list: list[dict] = self.__get_payment_info()
        sorting_key = 'payable_amount'
        
        for m in [('minimum', min), ('maximum', max)]:
            info[m[0]] = m[1](
                payment_info_list, key=lambda x: x.__dict__[sorting_key])
        
        return ditto(info)
