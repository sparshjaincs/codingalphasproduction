from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="discuss_homepage"),
    path("quora_submit/",views.quora_submit,name="quora_submit"),
    path("<method>/inbox/<id>/",views.inside,name='inside'),
]