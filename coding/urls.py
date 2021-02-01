from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="coding"),
    path("practise/<title>/<ins>/",views.inside,name="inside"),
    path('filter/ajax/table/',views.filter,name="filter"),
    path('template/ajax/<id>/',views.template,name="template"),
    path('save/ajax/<id>/',views.save,name="save"),
    path('test/ajax/<id>/',views.runcode,name="runcode"),
    path('like/ajax/',views.like,name="like"),
    path('list/ajax/',views.list,name="list"),
]