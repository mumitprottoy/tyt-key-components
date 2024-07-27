from django.contrib import admin
from .models import TherapyType, TherapyTypeMember, DASS21Statements

admin.site.register([DASS21Statements])


@admin.register(TherapyType)
class TherapyTypeAdmin(admin.ModelAdmin):
    list_display = ('readable_name', 'code_name')


@admin.register(TherapyTypeMember)
class TherapyTypeMemberAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'therapy_type')


