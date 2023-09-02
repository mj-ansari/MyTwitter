from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('', index, name='home'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile/followers/<int:pk>', followers, name='followers'),
    path('profile/follows/<int:pk>', follows, name='follows'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('update_user/', update_user, name='update_user'),
    path('tweet_like/<int:pk>', tweet_like, name='tweet_like'),
    path('tweet_share/<int:pk>', tweet_share, name='tweet_share'),
    path('tweet_delete/<int:pk>', tweet_delete, name='tweet_delete'),
    path('tweet_edit/<int:pk>', tweet_edit, name='tweet_edit'),
    path('unfollow/<int:pk>', unfollow, name='unfollow'),
    path('follow/<int:pk>', follow, name='follow'),
    path('search/', search, name='search'),
]
