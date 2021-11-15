from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from .models import Comments, Followers, User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import EmptyPage, Paginator
import json

from datetime import datetime

def index(request):
    comments = Comments.objects.order_by('-comment_time')

    try:
        user_id = User.objects.get(pk=request.user.id)
    except:
        user_id = "none"

    pages = Paginator(comments,10)
    
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)

    return render(request, "network/index.html", {
        "page_obj": page,
        "user_id": user_id
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
            comment_time = datetime.now(),
            number_of_likes = 0
        )

        try:
            post.save()
        
        except:
            print("Error in database comment")
        
        comments = Comments.objects.order_by('-comment_time')

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/new_post.html", {"user_id": request.user.id})


def profile(request, user_id):

    same_user = False
    #print(f"aqui estoy {int(user_id) == int(request.user.id)}")
    if ( int(user_id) == int(request.user.id) ):
        same_user = True
      
    
    user_profile = User.objects.get(pk=user_id)
    comments = Comments.objects.filter(user_id = user_id).order_by('-comment_time')

    #because I dont have a lot of users,instead of doing the logic myself, I do it in the DB
    following = len(Followers.objects.filter(user_id=user_id))
    followers = len(Followers.objects.filter(follower=user_id))

    testing = Followers.objects.filter(follower=user_id)
    print(testing)

    already_follow = len(Followers.objects.filter(user_id=request.user.id).filter(follower=user_id))
    if already_follow == 1:
        follow_status = "Unfollow"
    else:
        follow_status = "Follow"

    pages = Paginator(comments,10)
    
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)
  
    return render(request, "network/profile.html",{
                "page_obj": page,
                "user_profile": user_profile,
                "user_id": request.user.id,  
                "same_user": same_user,
                "following": following,
                "followers": followers,
                "follow_status": follow_status
                
                })
        

def followers(request):

    if request.method == "POST":
       
        follow_action = request.POST["follow_action"]
        to_follow_id = int(request.POST["user_id"])

        if follow_action == "Follow":
      
            user_follower = Followers.objects.filter(user_id=request.user.id).filter(follower = to_follow_id)
            print(user_follower)
            if len(user_follower) == 0:
                #agregar comprobacion de que no sea el mismo user quien se siga
                new_follower = Followers.objects.create(
                    user_id = User.objects.get(pk=request.user.id),
                    follower = User.objects.get(pk=to_follow_id)
                )

                try:
                    new_follower.save()
                
                except:
                    print("Error in database comment")
                    #return JsonResponse({"error": "GET or PUT request required."}, status=400)
                
            return HttpResponseRedirect(reverse("index"))
        
        else:
            try:
                user_follower = Followers.objects.filter(user_id=request.user.id).get(follower = to_follow_id)
                user_follower.delete()
                print("deleting.............................")
            except:
                print("Error while deleting user")
            
            return HttpResponseRedirect(reverse("index"))

def following(request):

    user_id = User.objects.get(pk=request.user.id)
    following = Followers.objects.filter(user_id=user_id)
    paginar = []
    all_following_comments= []

    for seguidores in following:
        comments = Comments.objects.filter(user_id = seguidores.follower).order_by('-comment_time')
        all_following_comments.append(comments)

    #print(all_following_comments)
    for level_comment in all_following_comments:
        for comments in level_comment:
            paginar.append(comments)

    pages = Paginator(paginar,10)
    
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)

    return render(request,"network/pages.html", {"page_obj": page})
    #return render(request,"network/follows_comment.html", {"all_comments": all_following_comments})

@csrf_exempt
@login_required
def edit_post(request):

    if request.method == 'POST':
        try:
            comment = json.loads(request.body)
        except:
            comment = 999

        print(comment['comment_id'])

        to_edit = Comments.objects.get(pk = comment['comment_id'])

        
        #print(test)
        return JsonResponse(to_edit.serialize(), safe=False)

    elif request.method == 'PUT':

        try:
            comment = json.loads(request.body)
        except:
            return JsonResponse({"message": "Error, while updating"}, safe=False)

        print(comment['new_comment'])

        to_update = Comments.objects.get(pk = comment['comment_id'])

        user = User.objects.get(pk=request.user.id)
        print(user)
        print(to_update.user_id)
        if (user == to_update.user_id):
            to_update.comment = comment['new_comment']
            to_update.save()
        else:
            return JsonResponse({"message": "not authorize user"}, safe=False)

       

        return JsonResponse(to_update.serialize(), safe=False)

@csrf_exempt
@login_required
def like_post (request):
    if request.method == 'POST':
        try:
            comment = json.loads(request.body)
        except:
            comment = 999

        print(comment['comment_id'])

#-------------------------------------------------------------------------------#

        user = User.objects.get(pk= request.user.id)

        post = Comments.objects.get(pk = comment['comment_id'])

        post.number_of_likes = post.likes.count()
        post.save()

        if post in user.all_liked_post.all():
            post.likes.remove(user)
            post.number_of_likes = post.number_of_likes  - 1
           
        
        else:
            post.likes.add(user)
            post.number_of_likes = post.number_of_likes  + 1
        
        post.save()
        return JsonResponse({"likes": post.number_of_likes}, safe=False)