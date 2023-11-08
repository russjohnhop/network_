from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
from .models import User, Post, PostForm
from django.core.paginator import Paginator
import json
from django.conf import settings
from django.utils.timezone import make_aware


def index(request):

    naive_datetime = datetime.now()

    aware_datetime = make_aware(naive_datetime)

    if request.user.is_authenticated:
        # posts = Post.objects.all().filter(username = request.user)
        posts = Post.objects.all().order_by('-timestamp')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        if request.method == "POST" :
            post = Post.objects.create(
                username = request.user,
                post_content = request.POST["post_content"],
                timestamp = aware_datetime
            )
            return render(request, "network/index.html", {
                "form" : PostForm(),
                "posts" : page_obj
            }
            )
        if request.method == "GET":
            return render(request, "network/index.html", {
                "form" : PostForm(),
                "posts" : page_obj
            })
    
    else:
        return HttpResponseRedirect(reverse("login"))
    



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

@csrf_exempt
@login_required
def profile(request, username):
        profile_user = User.objects.get(username=username)
        viewer_user = request.user
        followers = profile_user.followers.all()
        follows = profile_user.following.all()
        user_id = profile_user.id
        user_posts = Post.objects.filter(username=user_id).order_by('-timestamp')
        paginator = Paginator(user_posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        if User.objects.filter(username=viewer_user, following=profile_user).exists():
            is_following = True
        else:
            is_following = False

        print(is_following)

        return render(request, "network/profile.html", {
            "followers": followers,
            "follows" : follows,
            "profile_user" : profile_user,
            "is_following" : is_following,
            "posts" : page_obj,
            "username" : username,
            "viewer_user" : viewer_user
        })

# Hybrid follow/following posts page function

@login_required
def following(request):
    active_user = request.user
    if request.method == "GET":
        user = User.objects.get(username=active_user)
        following = user.following.all()
        posts = Post.objects.filter(username__in=following).order_by('-timestamp')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/following.html", {
            "posts" : page_obj
        })
    
    if request.method == "POST":
        profile_user = request.POST["follow_user"]
        print('Profile user in the following function is' + profile_user)

        follow_user = User.objects.filter(username = active_user, following = profile_user)
        active_user = User.objects.get(username=active_user)
        profile_user = User.objects.get(id=profile_user)

        if follow_user.exists():

            active_user.following.remove(profile_user)
            profile_user.followers.remove(active_user)
            active_user.save()
        else:

            active_user.following.add(profile_user)
            profile_user.followers.add(active_user)
            active_user.save()
            profile_user.save()

        username = profile_user.username
        return redirect('profile', username=username)
    
@csrf_exempt
@login_required
def post(request, post_id):

    naive_datetime = datetime.now()

    aware_datetime = make_aware(naive_datetime)


    # Query for requested post
    try: 
        post = Post.objects.get(username=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
        
    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":

            try:
                post_data = json.loads(request.body)
                post_content = post_data.get("post_content")

                if post_content:
                    post.post_content = post_content
                    post.timestamp = aware_datetime

                post.save()
            
            except ValueError:
                return JsonResponse({"Forbidden": "Values not entered"}, status=403)
            return HttpResponse(status=200)


    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)



@csrf_exempt
def update_likes(request,post_id):
    print("update_likes function is running")

    # Handle the update of the model etc:

    user = request.user
    current_post = Post.objects.get(pk=post_id)

    # Retrieve a list of users who liked the post

    user_likes = current_post.likes.all()


    if user in user_likes:
        current_post.likes.remove(user)
        print("user added")
    else:
        current_post.likes.add(user)
        print("user removed")

    return JsonResponse(current_post.serialize())

    

