from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms


def index(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Your Tweet Has Been Posted !")
                return redirect("home")

        tweets = Tweet.objects.all().order_by("-created_at")
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "index.html", {"tweets": tweets, "form": form, "profiles": profiles})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, "index.html", {"tweets": tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, "profile_list.html", {"profiles": profiles})
    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get("follow")
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
                messages.warning(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
            elif action == "follow":
                messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, "profile.html", {"profile": profile, "tweets": tweets})

    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "followers.html", {"profiles": profiles})
        else:
            messages.warning(request, "Not Your Page !!")
            return redirect("home")
    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, "follows.html", {"profiles": profiles})
        else:
            messages.warning(request, "Not Your Page !!")
            return redirect("home")
    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.warning(
            request, (f"You Have Successfully Unfollowed {profile.user.username}")
        )
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(
            request, (f"You Have Successfully Followed {profile.user.username}")
        )
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In , Keep Tweeting !!")
            return redirect("home")
        else:
            messages.error(
                request, "Wrong Username or Password, Please try Again !!"
            )
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out , See You Again !!")
    return redirect("home")


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Been Registered Successfully !!")
            return redirect("home")
    return render(request, "register.html", {"form": form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        user_form = SignUpForm(
            request.POST or None, request.FILES or None, instance=current_user
        )
        profile_form = ProfilePicForm(
            request.POST or None, request.FILES or None, instance=profile_user
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, "Your Profile Has Been Updated Successfully !!")
            return redirect("home")
        return render(
            request,
            "update_user.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
    else:
        messages.warning(request, "You Must Be Logged In To View This Page")
        return redirect("home")


def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.warning(request, "You Must Be Logged In To Like A Tweet !!")
        return redirect("home")


def tweet_share(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet:
            return render(request, "tweet_share.html", {"tweet": tweet})
        else:
            messages.error(request, "Tweet Does Not Exist !!")
            return redirect("home")
    else:
        messages.warning(request, "You Must Be Logged In To Share A Tweet !!")
        return redirect("home")


def tweet_delete(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
            tweet.delete()
            messages.success(request, "Tweet has Been Deleted !!")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, "Not Your Tweet Stupid !!")
            return redirect("home")
    else:
        messages.warning(request, "Please Log In To Continue...")
        return redirect("home")


def tweet_edit(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
            form = TweetForm(request.POST or None, instance=tweet)
            if request.method == "POST":
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, "Your Tweet Has Been Updated !")
                    return redirect("home")
            else:
                return render(
                    request, "tweet_edit.html", {"form": form, "tweet": tweet}
                )
        else:
            messages.success(request, "Not Your Tweet Stupid !!")
            return redirect("home")
    else:
        messages.warning(request, "Please Log In To Continue...")
        return redirect("home")


def search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        if search.startswith(" ") or len(search) < 2:
            messages.warning(request, "Provide Some Unique Words !!")
            return redirect(request.META.get("HTTP_REFERER"))
        search_tweet = Tweet.objects.filter(body__icontains=search)
        search_user = User.objects.filter(username__icontains=search)
        return render(
            request,
            "search.html",
            {
                "search": search,
                "search_tweet": search_tweet,
                "search_user": search_user,
            },
        )
    else:
        return render(request, "search.html", {})
