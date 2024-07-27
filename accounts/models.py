from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from utils.key_generator import KeyGen
from datetime import datetime



class AdditionalInfoFlag(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added = models.BooleanField(default=False)
    
    def __str__(self): return self.user.username 
    

class PasswordResetMode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_on = models.BooleanField(default=False)
    
    def turn_on(self):
        self.is_on = True; self.save()
    
    def turn_off(self):
        self.is_on = False; self.save()
    
    def __str__(self): return self.user.username 
    


class EmailVerificationFlag(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    
    def __str__(self): return self.user.username 
    


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.TextField()
    
    def __str__(self): return self.user.username



class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(_("Email address"), max_length=254, default="N/A")
    phone_number = models.CharField(max_length=50, default="N/A")
    
    
    def save(self, *args, **kwargs):
        if self.email != self.user.email:
            self.email = self.user.email
        
        super().save(*args, **kwargs)
        
    
    class Meta:
        verbose_name_plural = "Contact Info"
    
    def __str__(self) -> str:
        return self.user.username



class PersonalInfo(models.Model):
    MALE = "Male"; FEMALE = "Female"; OTHER = "Other"
    GENDER_CHOICES = (
        (MALE, MALE), (FEMALE, FEMALE), (OTHER, OTHER),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=MALE)
    birth_year = models.IntegerField(default=2000)
    
    
    @staticmethod
    def get_birth_year_choices() -> list:
        y = datetime.today().year - 11
        return [yr for yr in range(y-100, y)[::-1]]


    def validate_birth_year(self, birth_year: int) -> bool:
        return birth_year in self.get_birth_year_choices()
    

    def get_age(self) -> int:
        from datetime import datetime
        return datetime.today().year - self.birth_year
    
    def get_gender_icon_class(self):
        return {'Male': 'fa fa-mars', 
        'Female': 'fa fa-venus',
        'Other': 'fa fa-genderless'
        }[self.gender]

    def get_age_str(self) -> str:
        return f'{self.get_age()} years'
    

    class Meta:
        verbose_name_plural = "Personal info"
    

    def __str__(self) -> str:
        return self.user.username
    


class UserGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def create_default_user_groups():
    from utils import defaults
    for name in defaults.USER_GROUP_NAMES:
        if not UserGroup.objects.filter(name=name).exists():
            new = UserGroup(name=name); new.save()

create_default_user_groups()



class UserGroupMember(models.Model):
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'member'],
                name='duplicate_group_member' 
            )
        ]

    
    def __str__(self):
        return self.member.username 
    


class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)


    class Meta:
        verbose_name = 'Verification Code'
        verbose_name_plural = 'Verification Code'

    @staticmethod
    def generate_code():        
        return KeyGen().num_key(length=6)


    def update_code(self):
        self.code = self.generate_code()
        self.save()

    
    def __str__(self) -> str:
        return self.user.username
    


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)


    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTP'

    @staticmethod
    def generate_code():        
        return KeyGen().num_key(length=6)


    def update_code(self):
        self.code = self.generate_code()
        self.save()

    
    def __str__(self) -> str:
        return self.user.username







class MagicKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verification_key = models.CharField(max_length=200)
    password_reset_key = models.CharField(max_length=200)


    def __generate_magic_key(self) -> str:
        keygen = KeyGen()
        key = keygen.datetime_key()
        key += str(self.user.id)
        key += keygen.alphanumeric_key(length=69)

        return key
    

    def update_key(self, attr:str, save: bool=True):
        self.__dict__[attr] = self.__generate_magic_key()
        if save: self.save() 
        return self.__dict__[attr]
    

    def verify(self, attr:str, key:str):
        return self.__dict__[attr] == key
        

    def __str__(self) -> str:
        return self.user.username