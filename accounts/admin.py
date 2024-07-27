from django.contrib import admin
from .models import (
    AdditionalInfoFlag, ContactInfo, PersonalInfo, 
    UserGroup, UserGroupMember, VerificationCode, 
    MagicKey, ProfilePicture, OTP, EmailVerificationFlag, PasswordResetMode)


@admin.register(AdditionalInfoFlag)
class AdditionalInfoFlagAdmin(admin.ModelAdmin):
    list_display = ('user', 'added')


@admin.register(PasswordResetMode)
class PasswordResetModeAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_on')
    
    
@admin.register(EmailVerificationFlag)
class EmailVerificationFlagAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified')


@admin.register(UserGroupMember)
class UserGroupMemberAdmin(admin.ModelAdmin):
    list_display = ('member', 'group')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin): 
    list_display = ('user', 'email', 'phone_number')


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birth_year')


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')




admin.site.register([
    UserGroup, MagicKey, ProfilePicture
])