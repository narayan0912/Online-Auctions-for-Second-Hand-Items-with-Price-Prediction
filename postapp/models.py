from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import random, string, pytz


from userapp.models import UserProfile



# Create your models here.


# creates a random letter/number slug
def generate_slug():
    while True:
        letters = string.ascii_letters
        slug = ''.join(random.choice(letters) for i in range(10))
        if Post.objects.filter(slug=slug):
            continue
        else:
            return slug
        
# 'post' table in database
class Post(models.Model):
     # function to make new name for images       
    def namecomFile1(self, filename):
        return '/'.join([f"{self.category}_pics", str(self.slug), 'comp_pic.jpg'])
    
    def nameFile1(self, filename):
        return '/'.join([f"{self.category}_pics", str(self.slug), f'optional_pic{1}.jpg'])
    def location(self):
        usrp = UserProfile.objects.filter(user=self.user).first()
        location = usrp.primary_location
        return location

    slug = models.CharField(default=None, max_length=16)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    category = models.CharField(max_length=255, default='Any')
    description = models.TextField(null=True)
    comp_image = models.ImageField(upload_to=namecomFile1,null=True)
    sell_location = models.CharField(default='any', max_length=128)

    sold = models.BooleanField(default=False)
    winner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=None)

    bidstart = models.IntegerField(default=0)
    buynow = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=datetime.now())
    date_end = models.DateTimeField(default=None)

    # to identify if the post is available or not
    @property
    def is_available(self):
        utc = pytz.UTC
        if self.sold or self.date_end.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc) and self.date_end is not None:
            return False
        return True

    def __str__(self) -> str:
        return self.title
    # async def bid_timeout_code(self):
    #     from bidapp.models import Bid
    #     bidobj = Bid.objects.filter(Post=self).order_by('amount', 'datetime').first()
    #     if bidobj is not None:
    #         self.winner = bidobj.participant
    #         self.sold = True
        
    # async def create_time_handler(self):
    #     import asyncio
    #     end = datetime.strptime(self.date_end, "%Y-%m-%dT%H:%M")
    #     scheduler = BlockingScheduler()
    #     scheduler.add_job(self.bid_timeout_code, 'date', run_date=end)
    #     loop = asyncio.get_event_loop()
    #     scheduler.start()
    #     try:
    #         loop.run_forever()
    #     except KeyboardInterrupt:
    #         pass
    #     finally:
    #         loop.close()

    
    