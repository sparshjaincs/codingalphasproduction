from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="coding"),
    path("practise/<title>/<ins>/",views.inside,name="inside"),
]