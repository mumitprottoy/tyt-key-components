import requests
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from utils.models import Tracker
from utils.operations import resolve_trx_check_url
from therapists.models import TherapistProfilePicture
from finances.models import Invoice, PaymentInfo, Promo, PromoRetrievalCount
from appointments.models import Appointment
from accounts.models import (
    AdditionalInfoFlag, EmailVerificationFlag, PasswordResetMode)
from emails.engine import EmailEngine
from accounts.models import UserGroup, UserGroupMember
from tytfs.models import StudentClub, StudentClubMember, StudentClubEmailLead



try:
    
    # An appointment can only be confirmed if the financial transaction is closed
    # An invoice transaction will be closed if the necessary payments (if payable) are done
    @receiver(post_save, sender=Invoice)
    def confirm_appointment(instance: Invoice, *args, **kwargs):
        invoice = instance
        if invoice.is_closed and invoice.tracker.appointment is not None:
            invoice.tracker.appointment.confirm()
    
    
    # If the user fails to make the necessary payments within a certain timeframe (denoted as APNT_HOLD_LIMIT)
    # the appointment will automatically be cancelled. Deleting the tracker will delete
    # both the appointment and the invoice
    @receiver(post_save, sender=Appointment)
    def delete_tracker(instance: Appointment, created, *args, **kwargs):
        apnt = instance
        
        if created:
            from interface.tasks.scheduled_tasks import execute_scheduled_task
            
            # This function will be called as a scheduled task after APNT_HOLD_LIMIT seconds
            # If the appointment is not confirmed by then
            def _del_tracker(tracker_key=apnt.tracker.key):
                tracker = Tracker.objects.get(key=tracker_key)
                _apnt = Appointment.objects.get(tracker=tracker)
                
                if _apnt.status == Appointment.PENDING:
                    invoice = Invoice.objects.get(tracker=tracker)
                    response = requests.get(resolve_trx_check_url(invoice.transaction_id)).json()
                    
                    if 'pay_status' in response and response['pay_status'] == 'Successful':
                        # payment is done, abort deletion
                        return None
                    
                    print('Deleting tracker', tracker.key, 'after', _apnt.get_secs_past(), 'seconds')
                    return tracker.delete()
                    
            from utils.constants import APNT_HOLD_LIMIT as timer
            execute_scheduled_task(timer=timer, task=_del_tracker)
            
    
    
    # Send emails with appointment status
    @receiver(post_save, sender=Appointment)
    def apnt_email(instance: Appointment, *args, **kwargs):
        apnt = instance
        if apnt.status == Appointment.CONFIRMED and (not apnt.email_sent):
            engine = EmailEngine(
                operation='confirm_appointment', 
                context={'apnt': apnt}, 
                recipient_list=[apnt.client.email, apnt.therapist.user.email],
                subject_code=f'Slot: {apnt.get_slot_str()}',
                notify_office=True
            )
            engine.send()
        else:
            # send booking email
            pass
    
    
    # Welcome the user
    @receiver(post_save, sender=User)
    def welcome_user(instance: User, created: bool, *args, **kwargs):
        user = instance
    
        # if created:
        #     email = EmailEngine(
        #         recipient_list=[user.email], operation='welcome')
        #     email.send()
            
    

    # Create the codes needed to verify email and reset password
    @receiver(post_save, sender=User)
    def create_codes(instance: User, created: bool, *args, **kwargs):
        user = instance

        if created:
            from accounts.models import VerificationCode, OTP
            VerificationCode(user=user, code=VerificationCode.generate_code()).save()
            OTP(user=user, code=OTP.generate_code()).save()
            


    # Every new user must have a randomly chosen profile picture, they can change it later
    @receiver(post_save, sender=User)
    def set_profile_picture(instance: User, created: bool, *args, **kwargs):
        user = instance

        if created:
            from random import randint
            from accounts.models import ProfilePicture
            url = 'https://images.theyellowtherapist.com/pp/'+str(randint(1,23))+'.jpg'
            ProfilePicture(user=user, url=url).save()
            

    
    # if a user is a therapist, it should have the therapist profile picture
    @receiver(post_save, sender=TherapistProfilePicture)
    def update_profile_picture(instance: TherapistProfilePicture, created: bool, *args, **kwargs):
        ttp = instance; url = ttp.url

        if created:
            ttp.therapist.user.profilepicture.url = url            
            ttp.therapist.user.profilepicture.save()            

    
    

    # Create Contact and Personal Info
    @receiver(post_save, sender=User)
    def create_contact_info(instance: User, created: bool, *args, **kwargs):
        user = instance
        
        if created:
            from accounts.models import ContactInfo, PersonalInfo
            ContactInfo(user=user).save(); PersonalInfo(user=user).save()
                     


    # Every user must be related to these flags and modes       
    @receiver(post_save, sender=User)
    def create_flags_and_modes_for_new_user(instance: User, created: bool, *args, **kwargs):
        user = instance
        
        if created:
            AdditionalInfoFlag(user=user).save()
            EmailVerificationFlag(user=user).save()
            PasswordResetMode(user=user).save()
    


    # If email is changed in User model, it must also reflect in ContactInfo
    @receiver(post_save, sender=User)
    def update_contactinfo_email(instance: User, *args, **kwargs):
        user = instance

        if user.email != user.contactinfo.email:
            user.contactinfo.email = user.email
            user.contactinfo.save()
    
    

    @receiver(post_save, sender=Promo)
    def create_promo_retrieval_count(instance: Promo, *args, **kwargs):
        promo = instance
    
        if bool(promo.user_retrieval_limit):
            for user_group in UserGroupMember.objects.filter(
                group=promo.user_group):
                if not PromoRetrievalCount.objects.filter(
                    user=user_group.member, 
                    promo=promo).exists():
                    prc = PromoRetrievalCount(
                        user=user_group.member, 
                        promo=promo, 
                    ); prc.save()
                    
                    """ if user_retrieval_limit is added after creating the
                    Promo (not while creating the Promo), check for the clients
                    that already used the promo without incrementing the
                    user_retrieval_count. Increment if found.
                        
                    """
                    for pi in PaymentInfo.objects.filter(
                        client=user_group.member, applied_promo=promo).all():
                            prc.count += 1; prc.save()
        
    
    @receiver(post_save, sender=PaymentInfo)
    def update_promo_count(instance: PaymentInfo, *args, **kwargs):
        payment_info = instance; promo = instance.applied_promo
        
        if promo is not None:
            promo.retrieval_count += 1; promo.save()
            if bool(promo.user_retrieval_limit):
                prc = PromoRetrievalCount.objects.get(
                    promo=promo, user=payment_info.client)
                prc.count += 1; prc.save()
    
    
    
    # Every user must be a member of "Everyone" UserGroup
    @receiver(post_save, sender=User)
    def add_new_user_to_everyone_group(instance: User, created: bool, *args, **kwargs):
        user = instance
        
        if created:
            UserGroupMember(
                group=UserGroup.objects.get(name='Everyone'), member=user).save()
        
        
        
    
    # *** NOTE *** 
    # A user must NOT be MANUALLY added to any university club (StudentClub) as a member
    
    
    # For every StudentClub instance, there must exist a UserGroup with the same name (acronym)
    @receiver(post_save, sender=StudentClub)
    def create_user_group_with_club_name(instance: StudentClub, created, *args, **kwargs):
        club = instance
        
        if created and not UserGroup.objects.filter(name=club.acronym).exists():
                UserGroup(name=club.name).save()    
    
    
    
    
    # *** NOTE ***
    # Addition of a user to a StudentClub as a member can only happen if the user's 
    # email matches an email from StudentClubEmailLead
    
    """A user can be added in a StudentClub as member in two cases:
            1) The user signed up with an email matching the lead
            2) The generated email lead already belonged to an existing user
    """
    
    # 1) The user signed up with an email matching the lead 
    @receiver(post_save, sender=User)
    def add_new_user_to_student_club(instance: User, created: bool, *args, **kwargs):
        user = instance
        
        if created and StudentClubEmailLead.objects.filter(email=user.email).exists():
                scel = StudentClubEmailLead.objects.get(email=user.email)
                scel.signed_up = True; scel.save()
                
                # Adding user to its club, where it belongs
                StudentClubMember(club=scel.club, member=user).save()
                
    
    
    # 2) The generated email lead already belonged to an existing user
    @receiver(post_save, sender=StudentClubEmailLead)
    def add_existing_user_to_student_club(instance: StudentClubEmailLead, created, *args, **kwargs):
        lead = instance
        
        if created and User.objects.filter(email=lead.email).exists():
            user = User.objects.get(email=lead.email)
            lead.signed_up = True; lead.save()
            
            # Adding user to its club, where it belongs
            StudentClubMember(club=lead.club, member=user).save()
    
    
    
    # A StudentClubMember must be a member of the UserGroup of same name (acronym)
    @receiver(post_save, sender=StudentClubMember)
    def add_student_club_member_to_corresponding_user_group(instance: StudentClubMember, created, *args, **kwargs):
        member = instance
        
        if created and not UserGroupMember.objects.filter(
                group=UserGroup.objects.get(
                    name=member.club.acronym), member=member.member).exists():
            UserGroupMember(
                group=UserGroup.objects.get(
                    name=member.club.acronym), member=member.member).save()
    
    
    
    # If a user is a member of a StudentClub it must be a member of "Student" UserGroup
    @receiver(post_save, sender=StudentClubMember)
    def add_student_club_member_to_student_group(instance: StudentClubMember, created, *args, **kwargs):
        club = instance
        
        if created and not UserGroupMember.objects.filter(
                group=UserGroup.objects.get(
                    name='Student'), member=club.member).exists():
            UserGroupMember(group=UserGroup.objects.get(
                    name='Student'), member=club.member).save()
                
    
except Exception as exec: print(exec)     
 
    