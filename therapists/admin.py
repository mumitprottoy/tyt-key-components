from django.contrib import admin
from .models import *


@admin.register(TherapistExperience)
class TherapistExperienceAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'year_started')



@admin.register(TherapistExpertise)
class TherapistExpertiseAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'field')



@admin.register(TherapistMeetingLink)
class TherapistMeetingLinkAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'link')



@admin.register(TherapistQualification)
class TherapistQualificationAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'qualification')



@admin.register(TherapistWorkplace)
class TherapistWorkplaceAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'workplace')


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_public')


admin.site.register([
    TherapistProfilePicture, 
    ExpertiseField
])