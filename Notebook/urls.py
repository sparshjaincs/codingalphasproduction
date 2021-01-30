from django.urls import path
from . import views
urlpatterns = [
    path("",views.notebook,name="notebook"),
    path("delete/<id>/",views.delete,name="delete"),
    path("edit/<id>/",views.edit,name="edit"),
]