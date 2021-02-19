from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("like/",views.like,name="like"),
     path("dislike/",views.dislike,name="dislike"),
     path("follow/",views.follow,name="follow"),
     path("mark/",views.mark,name="mark"),
     path("profile/<user>/",views.profile,name="profile")
]