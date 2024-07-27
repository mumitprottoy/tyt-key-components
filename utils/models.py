from django.db import models


class Tracker(models.Model):
    key = models.CharField(max_length=100)

    @staticmethod
    def generate_tracker_key():
        from utils.key_generator import KeyGen
        keygen = KeyGen()
        return keygen.tracker_key()

    def __str__(self) -> str:
        return self.key




class Policy(models.Model):
    title = models.CharField(max_length=100)
    copy = models.TextField(default='...')

    class Meta:
        verbose_name_plural = 'Policies'
        
    def __str__(self) -> str:
        return self.title