from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Register(AbstractUser):
    class Meta:
        verbose_name = "Register"          
        verbose_name_plural = "Register"
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('user',"User"),
    )
    Role=models.CharField(choices=ROLE_CHOICES,default='user')
    def __str__(self):
        return self.username
    
    
class Poll(models.Model):
    question=models.CharField()
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Option(models.Model):
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE,related_name='options')
    option_text=models.CharField()
    votes=models.IntegerField(default=0)

    def __str__(self):
        return self.option_text

class Vote(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    poll=models.ForeignKey(Poll,on_delete=models.CASCADE)
    option=models.ForeignKey(Option,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} voted for {self.option}"
    
    class Meta:
        unique_together=['user','poll']
# Create your models here.
