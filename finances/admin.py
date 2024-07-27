from django.contrib import admin
from .models import (
    BaseSessionFee, 
    PriceGroup, 
    PriceGroupTherapistMember,
    Commission,
    Invoice,
    Promo,
    PromoRetrievalCount,
    PaymentInfo
)



@admin.register(PriceGroup)
class PriceGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'therapy_type', 'user_group', 'commission', 'is_active')




@admin.register(PriceGroupTherapistMember)
class PriceGroupTherapistMemberAdmin(admin.ModelAdmin):
    list_display = (
        'therapist', 'group', 
        'first_session_therapist_discount', 
        'recurring_session_therapist_discount')



@admin.register(BaseSessionFee)
class BaseSessionFeeAdmin(admin.ModelAdmin):
    list_display = (
        'therapist', 'therapy_type', 'first_session', 'recurring_session')



@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_session', 'recurring_session')



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('client', 'tracker', 'transaction_id')
    search_fields = ('client', 'tracker', 'transaction_id')


@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('client', 'tracker', 'payable_amount')
    search_fields = ('client', 'tracker', 'payable_amount')



@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('name', 'therapy_type', 'user_group', 'is_active')



@admin.register(PromoRetrievalCount)
class PromoRetrievalCountAdmin(admin.ModelAdmin):
    list_display = ('promo', 'user', 'count', 'maxed_out')

    
    