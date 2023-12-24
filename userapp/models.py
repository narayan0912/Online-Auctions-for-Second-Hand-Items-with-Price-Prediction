from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
# Create your models here.

# inherits abstractuser to create a table necessary for storing 'user' 
class CustomUser(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email=models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email     


# makes table with the details given below 
class UserProfile(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # sets foreign key to primary key of user table
    full_name =models.CharField(max_length=255)
    primary_location = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=12)
    
    def __str__(self) -> str:
        return self.full_name


