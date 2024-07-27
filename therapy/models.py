from django.db import models
from django.utils.translation import gettext_lazy as _
from therapists.models import Therapist



class TherapyType(models.Model):
    readable_name = models.CharField(max_length=100, unique=True)
    code_name = models.IntegerField(default=0, unique=True)

    
    def __str__(self):
        return self.readable_name
    
    

class TherapyTypeMember(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    therapy_type = models.ForeignKey(TherapyType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.therapist.user.username


resolve_cover_pic_url = lambda code_name: f'https://images.theyellowtherapist.com/therapy-type/{code_name}.png'
therapy_type_data = {
    1 : {
        'cover_pic_url': resolve_cover_pic_url(1),
        'description': 'One-on-one sessions for me' 
    },
    2 : {
        'cover_pic_url': resolve_cover_pic_url(2),
        'description': 'Sessions for me and my partner'
    }
}




class DASS21Statements(models.Model):
    DEPRESSION = 'Depression'
    ANXIETY = 'Anxiety'
    STRESS = 'Stress'
    LABEL_CHOICES = (
        (DEPRESSION, DEPRESSION),
        (ANXIETY, ANXIETY),
        (STRESS, STRESS)
    )
    
    statement = models.TextField()
    label = models.CharField(max_length=20, choices=LABEL_CHOICES)
    
    class Meta:
        verbose_name = 'DASS-21 Test Statement'
        verbose_name_plural = 'DASS-21 Test Statements'
    
    def __str__(self): return self.statement