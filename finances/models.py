from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from therapists.models import Therapist
from accounts.models import UserGroup
from therapy.models import TherapyType
from utils.models import Tracker



class BaseSessionFee(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    therapy_type = models.ForeignKey(TherapyType, on_delete=models.CASCADE)
    first_session = models.IntegerField(_("First sessions (BDT)"), default=0)
    recurring_session = models.IntegerField(_("Recurring sessions (BDT)"), default=0)    
    
    def __str__(self) -> str:
        return self.therapist.user.username



class Commission(models.Model):
    name = models.CharField(max_length=50)
    first_session = models.IntegerField(_("For first sessions (%)"), default=25)
    recurring_session = models.IntegerField(_("For recurring sessions (%)"), default=25)
    
    class Meta:
        verbose_name_plural = 'Commission'
    
    
    def __str__(self):
        return self.name 



class PriceGroup(models.Model): 
    name = models.CharField(max_length=100, unique=True)
    therapy_type = models.ForeignKey(TherapyType, on_delete=models.CASCADE)
    commission = models.ForeignKey(
        Commission,   
        on_delete=models.CASCADE, 
    )
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    is_active = models.BooleanField(_("active"), default=True)
    description = models.TextField(default="...")
    
    
    def __str__(self):
        return self.name     



class PriceGroupTherapistMember(models.Model):
    group = models.ForeignKey(PriceGroup, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    first_session_therapist_discount = models.IntegerField(
        _("Discount for first sessions (%)"), 
        default=0
    )
    recurring_session_therapist_discount = models.IntegerField(
        _("Discount for recurring sessions (%)"), 
        default=0
    )
    
    def __str__(self):
        return self.therapist.user.username



class Invoice(models.Model):
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tracker = models.OneToOneField(
        Tracker, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    transaction_id = models.CharField(max_length=50, default='N/A')
    is_closed = models.BooleanField(default=False)
    

    def generate_transaction_id(self) -> str:
        from utils.key_generator import KeyGen
        return KeyGen().transaction_id()
        
    
    def update_transaction_id(self):
        self.transaction_id = self.generate_transaction_id()
        self.save()


    def close_transaction(self):
        self.is_closed = True
        self.save()


    def __str__(self):
        return self.transaction_id



class Promo(models.Model):
    name = models.CharField(max_length=100)
    therapy_type = models.ForeignKey(
        TherapyType, on_delete=models.DO_NOTHING, default=TherapyType.objects.get(code_name=1).id)
    user_group = models.ForeignKey(UserGroup, on_delete=models.DO_NOTHING)
    is_free = models.BooleanField(_('Free'), default=False)
    max_deductable_amount = models.IntegerField(default=0)
    retrieval_limit = models.IntegerField(
        default=0, help_text='If limit is zero (0) it means there is no limit.')
    retrieval_count = models.IntegerField(default=0)
    user_retrieval_limit = models.IntegerField(
        default=0, help_text='If limit is zero (0) it means there is no limit.')
    is_active = models.BooleanField(_('Active'), default=True)

    def save(self, *args, **kwargs):
        if bool(self.retrieval_limit):
            if self.retrieval_count >= self.retrieval_limit:
                self.is_active = False
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name



class PromoRetrievalCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    promo = models.ForeignKey(Promo, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=0)
    maxed_out = models.BooleanField(default=False)

    def update_count(self):
        if self.promo.is_active and (not self.maxed_out):
            self.count += 1
            self.promo.retrieval_count += 1
            self.promo.save(); self.save()

    def save(self, *args, **kwargs):
        if self.promo.user_retrieval_limit <= self.count:
            self.maxed_out = True
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.promo.name



class PaymentInfo(models.Model):
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, default=None)
    is_payable = models.BooleanField(default=True)
    payable_amount = models.IntegerField(default=0)
    display_price = models.IntegerField(default=0)
    payable_to_therapist = models.IntegerField(default=0)
    is_discounted = models.BooleanField(default=False)
    applied_discount = models.IntegerField(default=0)
    applied_promo = models.ForeignKey(
        Promo, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    applied_user_group = models.ForeignKey(
        UserGroup, 
        on_delete=models.DO_NOTHING, default=None)
    applied_price_group = models.ForeignKey(
        PriceGroup, 
        on_delete=models.DO_NOTHING, default=None)
    applied_commission = models.IntegerField(default=25)
    
    
    class Meta:
        verbose_name = 'Payment Info'
        verbose_name_plural = 'Payment Info'

    def __str__(self):
        return self.tracker.key
        


    
    