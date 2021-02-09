from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="blog"),
    path("create/",views.create,name="create"),
]