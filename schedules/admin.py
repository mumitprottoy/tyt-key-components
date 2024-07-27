from django.contrib import admin
from .models import TherapistSchedule


@admin.register(TherapistSchedule)
class TherapistScheduleAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'weekday', 'hour', 'minute', 'is_active')


