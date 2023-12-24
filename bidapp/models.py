from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from userapp.models import UserProfile 
from django.core.validators import MaxValueValidator, MinValueValidator
from postapp.models import Post
# Create your models here.

# stores bid and assosiates it with Post and Userprofie of bidder (similar to "many to many")
class Bid(models.Model): 
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # sets the post 
    participant = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # the bidder
    amount = models.IntegerField() # Bid amount
    datetime = models.DateTimeField(default=datetime.now())

    def save(self):
        # before saving checks if the bid amount is valid for the post
        if int(self.amount) < int(self.post.bidstart):
            raise ValueError('Bid cannot be less than minimum amount.')
        super().save()