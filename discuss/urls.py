from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="discuss_homepage")
]