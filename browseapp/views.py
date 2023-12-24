from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from userapp.models import UserProfile
from postapp.models import Post
# Create your views here.
 
# view for / url
def home(request):
    # gets user login status and sends for the template to decide what to render 
    auth_status = request.user.is_authenticated
    return render(request, 'browseapp/home.html', {'auth': auth_status}) # the auth status is for choosing which navbar to run

# view for /browse url
def browse(request):
    # gets auth status
    auth_status = request.user.is_authenticated
    # gathers all content
    all_content = Post.objects.filter().order_by('-id')[:10:-1]
    # gets the availabe posts from all content
    all_available_contents = list(filter(lambda obj: obj.is_available, all_content))
    # declares filtered_content and all_available_filtered_contents to be none
    filtered_content = None
    all_available_filtered_contents = None

    # checs if user is logged in
    if request.user.is_authenticated:
        # gets the profile of logged in user
        prof = UserProfile.objects.filter(user=request.user).first()
        # if profile is none then it redirects them to createprofile page 
        if prof is None:
            return redirect('createprofile')
        # gets location details from te users profile
        location = prof.primary_location
        # gets the contents with the same location as the user's location
        filtered_content = Post.objects.filter(sell_location=location, ).order_by('-id')[:10:-1] 
        # gets the available ones from filtered_contents of te user's location 
        all_available_filtered_contents = list(filter(lambda obj: obj.is_available, filtered_content))

        # removes the contents with users location in all_available_contents to avoid overlapping
        all_available_content = []
        for a in all_available_contents:
            if a.sell_location == location:
                pass
            else:
                all_available_content.append(a)
        all_available_contents = all_available_content
    # returns all data and renders the given template
    return render(request, 'browseapp/browse.html', {
            'auth': auth_status,
            'all': all_available_contents,
            'filtered':all_available_filtered_contents
        })
