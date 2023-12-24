from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import PostForm
from .models import Post
from userapp.models import UserProfile
from bidapp.models import Bid
import string,random, pickle,asyncio

# generates random string (slug) to associate with each post
def generate_slug():
    while True:
        letters = string.ascii_letters
        slug = ''.join(random.choice(letters) for i in range(10))
        # checks if the created slug is unique so it does not overlap 
        if Post.objects.filter(slug=slug):
            continue
        else:
            return slug

# view for /post url
@login_required # means if not logged in it redirects to login page
@csrf_protect
def post(request):
    # it extracts user objects from the request.
    prof = UserProfile.objects.filter(user=request.user).first() # uses userprofile object then finds the user profile associated with the extracted user

    # if the profile doesnot exist for the user then they are redirected to createprofile page
    if prof is None: 
        return redirect('createprofile')

    # this checks if the method is post, post method is usually used to post information to the database through the server
    if request.method == 'POST':

        # bunch of if statements to check if the received data is valid

        # checks if bidstart is smaller than the buynow button
        if int(request.POST['bidstart']) > int(request.POST['buynow']):
            messages.error(request, message='Logic error in bidstart and buynow amounts.')
            form = PostForm()
            return render(request, 'postapp/post.html', {'form': form, 'auth':True})
        
        # checks if category is valid or not
        if request.POST['category'] not in ['vehicle', 'electronics', 'digital-prod', 'real-eastate']:
            messages.error(request, message='Something wrong with the form please reload and try!')
            form = PostForm()
            return render(request, 'postapp/post.html', {'form': form})
        if not request.POST['endtime']:
            messages.error(request, message='please enter end time')
            form = PostForm()
            return render(request, 'postapp/post.html', {'form': form})
        # gathers all data and creates a post object to make changes in the database
        post = Post(user=request.user,
                    slug=generate_slug(),
                    title = request.POST['title'],
                    date_end = request.POST['endtime'],
                    category = request.POST['category'],
                    description = request.POST['Description'],
                    bidstart = request.POST['bidstart'],
                    buynow = request.POST['buynow'],
                    comp_image = request.FILES['comp_image'],
                    sell_location = request.POST['location'])
        slug = post.slug
       
        post.save() # saves the data in the database

        # asyncio.run(post.create_time_handler)

        return redirect('view', slug=slug) # redirects to view page of the post that has just been posted
    else: # if the request is not post
        form = PostForm()
    form = PostForm() # creates a form for the page
    # renders a page with the form
    return render(request, 'postapp/post.html', {'form': form, 'auth':True})

# view fro viewing a post
@csrf_protect
def view(request, slug):
    # gets the post object using the provided slug in a url
    post = Post.objects.filter(slug=slug).first()
    # gets the url for image of the post
    imageurl = f'/media/{post.category}_pics/{post.slug}/comp_pic.jpg'
    # returns the data by rendering the given template
    return render(request, 'postapp/view.html', {'item': post,'available':post.is_available, 'img': imageurl, 'auth': request.user.is_authenticated, 'selfpost':post.user == request.user, 'end':post.date_end})

# view for predicting car prices
@csrf_protect
def predict(request):
    # checks if the data is post
    if request.method == 'POST':
        # gathers the sent data
        present_price = float(request.POST['price'])
        car_age = int(request.POST['age'])
        seller_type = request.POST['seller']
        fuel_type = request.POST['fuel']
        transmission_type = request.POST['transmission']

        # changes some data into 1 and 0 for using the modal to predict
        if fuel_type == 'Diesel':
            fuel_type = 1
        else:
            fuel_type = 0

        if seller_type == 'Individual':
            seller_type = 1
        else:
            seller_type = 0

        if transmission_type == 'Manual':
            transmission_type = 1
        else:
            transmission_type = 0
        m = open('rf_model', 'rb') # opens the modal file
        model = pickle.load(m)  # load ml model
        # uses the modal and predicts the price
        prediction = model.predict([[present_price, car_age, fuel_type, seller_type, transmission_type]])
        output = round(prediction[0], 2)
        return render(request,'postapp/predictcar.html', {'output':f"{output} Lakh", 'auth':request.user.is_authenticated})
    return render(request,'postapp/predictcar.html', {'auth':request.user.is_authenticated})


class CarPricePredictView(APIView):
    # runs if the request is post
    def post(self, request):
        # gathers the sent data
        present_price = float(request.data['price'])
        car_age = int(request.data['age'])
        seller_type = request.data['seller']
        fuel_type = request.data['fuel']
        transmission_type = request.data['transmission']
        # changes some data into 1 and 0 for using the modal to predict
        if fuel_type == 'Diesel':
            fuel_type = 1
        else:
            fuel_type = 0

        if seller_type == 'Individual':
            seller_type = 1
        else:
            seller_type = 0

        if transmission_type == 'Manual':
            transmission_type = 1
        else:
            transmission_type = 0
        m = open('rf_model', 'rb') # opens the modal file
        model = pickle.load(m)  # load ml model
        # uses the modal and predicts the price
        prediction = model.predict([[present_price, car_age, fuel_type, seller_type, transmission_type]])
        # rounds out then returns
        output = int(round(prediction[0], 2) * 100000) # output is in lakh form, so it has to be multiplied
        return Response(f'{output}')
    
    