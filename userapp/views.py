from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .forms import UserCreationForm, CreateProfileForm
from .models import UserProfile
from bidapp.models import Bid
from postapp.models import Post

# Create your views here.

# view for /register url
@csrf_protect
def register(request):
    # checks if the request is POST
    if request.method == 'POST':
        # gets the data from post request and passes it through UserCreationForm 
        form = UserCreationForm(request.POST) # creates form object
        if form.is_valid(): # runs if the form is valid
            form.save() # saves the data in form to the database
            username = form.cleaned_data.get('username') #gets username from tyhe form
            messages.success(request, f"Hi, your account as '{username}' has been sucessfully created.")
            return redirect('login') # redirects to login page after creation
    else:
        # if request is not post
        form = UserCreationForm() # creates a from object
    # renders the given template with the form object
    return render(request, 'userapp/register.html', {'form': form, 'auth':request.user.is_authenticated})


# view for /create_profile url
@csrf_protect
@login_required # if not logged in sends back to login page
def create_profile(request):
    if request.method == 'POST': # checks if request is a post request
        # creates a profile object from post request's data
        prof = UserProfile(
            full_name=request.POST['fullname'],
            date_of_birth = request.POST['dob'],
            primary_location = request.POST['location'],
            phone_number = request.POST['phone_number'],
        )
        prof.user = request.user # sets user to be the logged in user
        prof.save() # saves the object to the database
        return redirect('viewprofile') # redirects to profile page

    return render(request, 'userapp/createprofile.html',{'auth':request.user.is_authenticated})

# view for /viewprofile url   this view is used to open the user's own profile 
@login_required # if not logged in sends back to login page
def view_profile(request):
    
    # gets details of the logged in user
    profile = UserProfile.objects.filter(user=request.user).first() # details from the profile table
    # if the profile doesn't exist sends back to profile creation page
    if not profile:
        return redirect('createprofile')
    joined_bids = Bid.objects.filter(participant=profile).all() # bids the user has joined
    posts = Post.objects.filter(user=request.user) # posts created by the user
    wonbids = Post.objects.filter(winner=profile).all() # bids the user won
    # declaring sellers and wonbid lists
    sellers = []
    wonbid = []
    # adds phone number of the seller to sellers respective to the posts in wonbid 
    for bid in wonbids:
        tuser = bid.user
        wonbid.append(bid.title)
        sellers.append(UserProfile.objects.filter(user=tuser).first().phone_number) 
    
    # renders details with given template
    return render(request, 'userapp/viewprofile.html',{'auth':request.user.is_authenticated,'cuser':request.user,'profile':profile, 'posts':posts,'own':True, 'bid':joined_bids, 'wonbid':list(zip(wonbid, sellers))})

# view for /profile   this is used to view other user's profile with their username
def profile(request, username):
    User = get_user_model()
    # gets user object from the provided username
    user = User.objects.filter(username=username).first()
    # if the user is viewing their own username, they will be redirected to their viewprofilepage
    own = request.user == user # checks if the username provided in url matches the username of the user requesting
    if own:
        return redirect('viewprofile') # redirects to their own profile 
    
    profile = UserProfile.objects.filter(user=user).first()
    # if the user doesnot exist 404 is sent
    if not profile:
        resp = HttpResponse.status_code(404)
        return resp
    posts = Post.objects.filter(user=user)
    # renders given template with the details below
    return render(request, 'userapp/viewprofile.html',{'auth':user.is_authenticated,'cuser':user, 'profile':profile,'posts':posts, 'own':own})
    