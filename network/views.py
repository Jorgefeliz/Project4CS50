from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from .models import Comments, Followers, User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

def index(request):
    comments = Comments.objects.order_by('-comment_time')

    return render(request, "network/index.html", {
        "comments": comments,
        "user_id": request.user.id
        })
  


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        user_id = User.objects.get(pk=request.user.id)
        comment = request.POST['comment']

        print(f"aqui estoy: {comment}")

        post = Comments.objects.create(
            user_id = user_id,
            comment = comment,
            comment_time = datetime.now()
        )

        try:
            post.save()
        
        except:
            print("Error in database comment")
        
        comments = Comments.objects.order_by('-comment_time')

        return render(request, "network/index.html", {
            "comments": comments,
            "user_id": request.user.id
            })

    else:
        return render(request, "network/new_post.html", {"user_id": request.user.id})


def profile(request, user_id):
    same_user = False

    #print(f"aqui estoy {int(user_id) == int(request.user.id)}")
    if ( int(user_id) == int(request.user.id) ):
        same_user = True
      

    user_profile = User.objects.get(pk=user_id)
   
    comments = Comments.objects.filter(user_id = user_id).order_by('-comment_time')

    return render(request, "network/profile.html",{
        "comments": comments,
        "user_profile": user_profile,
        "same_user": same_user,
        "user_id": request.user.id
         })
         
@csrf_exempt
@login_required
def followers(user_id):

    print("estoy aqui")    
    if request.method == "POST":
        new_follower = Followers.objects.create(
            user_id = User.objects.get(pk=request.user.id),
            Follower = User.objects.get(pk=user_id)
        )

        try:
            new_follower.save()
        
        except:
            print("Error in database comment")
            return JsonResponse({"error": "GET or PUT request required."}, status=400)

        return HttpResponse(status=204)


