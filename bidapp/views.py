from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .models import Bid

from userapp.models import UserProfile, CustomUser as User
from postapp.models import Post
# Create your views here.


# view for /bid url
@login_required # if not logged in redirects to login
def bid(request, slug):
    # gets the user object of the request of a logged in user
    user = request.user
    # gets the post from the given slug in url
    post = Post.objects.filter(slug=slug).first()
    if post.is_available == False:
        return redirect('view', slug=slug)
    # gets the profile of the logged in user
    prof = UserProfile.objects.filter(user=user).first()
    # declares msg to be none
    msg = None

    # checks if the request is a post request
    if request.method == "POST":
        # check if the user is the owner of the post
        if user == post.user:
            # returns 400 to avoid further errors
            resp = HttpResponse.status_code(400)
            return resp
        # gets bid amount from the request
        amount = request.POST['amount']
        # creates a bid object from given data
        newbid = Bid(post=post, participant=prof, amount=amount)
        # tries to save
        try:
            newbid.save()
        # if this error occurs 
        except ValueError:
            # then message is set to this but the data is not saved because of the below error
            msg = 'Bid cannot be less than minumun amount.'
    # returns the response data through rendered template.
    return render(request, 'bidapp/bid.html', {'item': post, 'auth':request.user.is_authenticated, 'selfbid': post.user == user,'running':post.is_available, 'mybid':bid, 'msg':msg})
    
# view fro /sell url
@login_required
def sell(request, slug):
    # gets the seller from request 
    seller = request.user
    # gets the post from provided slug
    post = Post.objects.filter(slug=slug).first()
    # if the seller and the user does not match
    if seller != post.user:
        resp = HttpResponse.status_code(402) # 402 error (not authorized) is sent 
        return resp
    # if the request is post 
    if request.method == "POST":
        # data from the post request is gathered
        pk = request.POST['pk'] # primary key of the bid winner
        post.sold = True # sets post to be sold and not available
        post.winner = UserProfile.objects.filter(pk=pk).first() # sets winner for the post
        post.save() # saves the above changes to the database

        # gets the slug from the post and redirects to the bid page
        slug = post.slug
        return redirect('bid',slug=slug)
    # gets the bid from other users
    bids = Bid.objects.filter(post=post).all()
    # returns the bid information by rendering the given template
    return render(request, 'bidapp/sell.html', {'bids': bids, 'post':post})
