from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(_("Public"), default=False)
    
    def __str__(self):
        return self.user.username



class ExpertiseField(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

def create_default_expertise_fields():
    from utils import defaults
    for name in defaults.EXPERTISE_FIELDS:
        if not ExpertiseField.objects.filter(name=name).exists():
            field = ExpertiseField(name=name)
            field.save()

create_default_expertise_fields()



class TherapistExpertise(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    field = models.ForeignKey(ExpertiseField, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['therapist', 'field'],
                name='duplicate_expertise_field' 
            )
        ]
    
    def __str__(self):
        return self.therapist.user.username
    
    
    
class TherapistExperience(models.Model):
    therapist = models.OneToOneField(Therapist, on_delete=models.CASCADE)
    year_started = models.IntegerField(default=datetime.today().year)

    def get_experience(self):
        return datetime.today().year - self.year_started + 1
    
    def get_experience_str(self):
        year = 'years' if self.get_experience() > 1 else 'year'
        return f'{self.get_experience()} {year}'
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['therapist', 'year_started'],
                name='duplicate_year' 
            )
        ]
    
    def __str__(self):
        return self.therapist.user.username



class TherapistProfilePicture(models.Model):
    therapist = models.OneToOneField(Therapist, on_delete=models.CASCADE)
    url = models.TextField()
    
    
    
    def __str__(self):
        return self.therapist.user.username
    
    
    
class TherapistWorkplace(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    workplace = models.CharField(max_length=250)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['therapist', 'workplace'],
                name='duplicate_workplace' 
            )
        ]
    
    def __str__(self):
        return self.therapist.user.username



class TherapistQualification(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=250)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['therapist', 'qualification'],
                name='duplicate_qualification' 
            )
        ]
    
    def __str__(self):
        return self.therapist.user.username



class TherapistMeetingLink(models.Model):
    therapist = models.OneToOneField(Therapist, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['therapist', 'link'],
                name='duplicate_link' 
            )
        ]
    
    def __str__(self):
        return self.therapist.user.username



        