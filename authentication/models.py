from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    mobile=models.CharField(max_length=15,null=True,blank=True)
    mobile_verified=models.BooleanField(default=False)
    email_verified=models.BooleanField(default=False)
    otp_mobile=models.CharField(max_length=10,null=True,blank=True)
    otp_email=models.CharField(max_length=10,null=True,blank=True)
    profile_image=models.ImageField(upload_to='profile_image', default='profile_image/default_image.png')



